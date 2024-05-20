# -*- coding: utf-8 -*-
from flask import Blueprint, current_app, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
from sqlalchemy.orm.attributes import flag_modified
from datetime import datetime, timedelta, timezone
from __init__ import create_app, db
from models import User, Idea, KnowledgeState, ChatLog
from datetime import datetime
import base64
import json
import os
import http.client
import openai
import requests

openai.api_key = My_OpenAI_key

DRQ = ["Interpretation", "Goal Orientation", "Causal Antecedent", "Causal Consequent", "Expectational", "Instrumental/Procedural", "Enablement(DR)"]
GDQ = ["Proposal/Negotiation", "Scenario Creation", "Ideation", "Method", "Enablement"]
GoodQuestionCategory = DRQ + GDQ + ["Evaluation", "Recommendation"]

main = Blueprint('main', __name__)


@main.route("/signup", methods=['POST'])
@cross_origin()
def signup():
    params = request.get_json()
    email = params['email']
    name = params['name']
    password = params['password']
    # photo = request.files["photo"]
    existUser = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    if existUser: # if a user is found, we want to redirect back to signup page so user can try again
        # flash('Email address already exists')
        return {"":""}
    # if photo:
    #     # uniq_filename = make_unique(photo.filename)
    #     # photo_path = join(current_app.config['UPLOAD_FOLDER'],"photo",uniq_filename)
    #     # photo.save(photo_path)       
    #     pass
    # else:
    new_user = User(
        email = email,
        name = name,
        password = generate_password_hash(password, method='sha256'),
        realPassword = password
    )
    db.session.add(new_user)
    db.session.commit()

    new_KnowledgeState = KnowledgeState(
        user_id = new_user.id,
        opportunity = "",
        consideration = "",
        knowledge = ""
    )

    new_ChatLog = ChatLog(
        user_id = new_user.id,
        log = []
    )

    new_ideas = [
        Idea(user_id=new_user.id, title="유아친화 지역 사회 공간", target_problem="아이를 키우는 환경의 부족", idea="지역 사회 내에서 안전하고 창의적인 유아친화 공간을 만들어 부모들이 아이들을 더욱 편리하고 즐겁게 키울 수 있도록 지원합니다. 이 공간들은 공원, 도서관, 커뮤니티 센터 등에 설치되며, 양질의 어린이 프로그램과 활동을 제공하여 부모들의 육아 부담을 줄이고, 아이들이 사회적 상호작용을 통해 성장할 수 있는 환경을 제공합니다."),
        Idea(user_id=new_user.id, title="플렉스 워크 포인트", target_problem="일과 가정의 균형 부족", idea="기업들이 육아와 일을 병행할 수 있도록 유연한 근무 환경을 제공하는 정책을 도입합니다. 이 아이디어는 육아 휴직, 시간 선택 근무, 재택 근무 옵션을 포함하여 부모가 자녀 양육에 더 많은 시간을 할애할 수 있게 돕습니다. 또한, 직장 내 어린이집을 설치하여 부모가 직장 근처에서 아이들과 더 많은 시간을 보낼 수 있게 합니다."),
        Idea(user_id=new_user.id, title="노인과 청년 연결 프로그램", target_problem="고령화 사회의 노인 인력 활용", idea="노인 세대가 자신의 지식과 경험을 청년 세대에게 전달할 수 있는 멘토링 및 지원 프로그램을 개발합니다. 이 프로그램은 노인을 일자리와 연결하여 활동적인 사회 생활을 유지하게 돕고, 동시에 젊은 부모나 예비 부모에게 육아와 관련된 지식과 지원을 제공합니다. 이러한 상호작용은 세대 간의 소통과 이해를 증진시키고, 고령화 사회에서의 노인들의 역할을 재정의합니다.")
    ]

    print(new_user.id)
    db.session.add_all(new_ideas)
    db.session.add(new_KnowledgeState)
    db.session.add(new_ChatLog)
    db.session.commit()

    return {"msg": "make account successful"}

@main.route("/token", methods=['POST'])
@cross_origin()
def create_token():
    params = request.get_json()
    email = params['email']
    password = params['password']
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Please sign up before!')
        return {"msg": "Wrong email or password"}, 401
    elif not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return {"msg": "Wrong email or password"}, 401

    db.session.commit()   

    access_token = create_access_token(identity=email)
    response = {"access_token":access_token}
    return response

@main.route("/logout", methods=["POST"])
@cross_origin()
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response
 

@main.route("/profile")
@jwt_required()
@cross_origin()
def profile():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    name = user.name
    ideasData = []
    ideas = Idea.query.filter_by(user_id=user.id).all()
    ideasData = [{"id": idea.id, "title": idea.title, "problem": idea.target_problem, "idea": idea.idea} for idea in ideas]
    userChat = ChatLog.query.filter_by(user_id=user.id).first()

    return {"ideasData": ideasData, "chatData": userChat.log, "name": name}

@main.route("/response", methods=["POST"])
@jwt_required()
@cross_origin()
def response():
    params = request.get_json()
    feedback = params['feedback']
    user = User.query.filter_by(email=get_jwt_identity()).first()
    ideasData = []
    ideas = Idea.query.filter_by(user_id=user.id).all()
    ideasData = [{"id": idea.id, "title": idea.title, "problem": idea.target_problem, "idea": idea.idea} for idea in ideas]
    user_knowledgestate = KnowledgeState.query.filter_by(user_id=user.id).first()
    opportunity = user_knowledgestate.opportunity
    consideration = user_knowledgestate.consideration
    knowledge = user_knowledgestate.knowledge
    user_chat = ChatLog.query.filter_by(user_id=user.id).first()

    goodQuestionChecker = False
    feedbackeval_prompt = [{"role": "system", "content":"Feedback Analysis Instructions for Instructor’s Review of a Student’s Design Idea.\nSTEP 1: Review previous ideas and chat logs to understand the context of the feedback.\nSTEP 2: Decompose the feedback into individual sentences.\nSTEP 3: Classify each sentence into one of two primary categories; Provoke Thought: This feedback aims to ensure that the feedback provider has a clear and accurate understanding of the design presented.; Provide Information: This feedback provides relevant information or is directly related to a design idea to evaluate or suggest improvements.\nSTEP 4: Subcategorize each sentence based on its nature (There are 21 types of ‘Provoke Thought’ and 3 types of ‘Provide information.’); Provoke Thought: Low-Level Question: Seeks factual details about the design. - Verification: Is X true? (e.g., \"Do they have TVs in the depots?\")\n- Definition: What does X mean? (e.g., \"What do you mean by 'best performance'?\")\n- Example: What is an example of X? (e.g., \"What would be three top use cases you can envision right now?\")\n- Feature Specification: What (qualitative) attributes does X have? (e.g., \"What kinds are they?\")\n- Concept Completion: Who? What? When? Where? (e.g., \"Where is the processing happening?\")\n- Quantification: How much? How many? (e.g., \"How many interact with your web app?\")\n- Disjunctive: Is X or Y the case? (e.g., \"Is it mobile or web from here?\")\n- Comparison: How does X compare to Y? (e.g., \"Tell me the difference between data from supply chain and sales\")\n- Judgmental: What is your opinion on X? (e.g., \"Do you think each hospital will use it for its own data?\")\nDeep Reasoning Question: Explores deeper implications or reasons behind the design.\n- Interpretation: How is a particular event or pattern of information interpreted or summarized? (e.g., \"What do you think the need is based on where they’re going?\")\n- Goal Orientation: What are the motives behind an agent’s action? (e.g. \"As far as the client, do you know what their main goal is?\")\n- Causal Antecedent: What caused X to occur? (e.g. \"What keeps the costs up?\")\n- Causal Consequent: What were the consequences of X occurring? (e.g. \"How did the new system affect their operations?\")\n- Expectational: Why is X not true? (e.g. \"Why does it not store historical data?\")\n- Instrumental/Procedural: How does an agent accomplish a goal? (e.g. \"How did you decide that these are the 3 tabs?\")\n- Enablement(DR): What object or resource enables an agent to perform an action? (e.g. \"Are there specific people that transport components? Is there a forklift driver and that’s his job?\")\nGenerate Design Question: Encourages innovative thinking about design challenges.\n - Proposal/Negotiation: Could a new concept be suggested/negotiated? (e.g. \"Do you think they’ll want to see some analytics?\")\n- Scenario Creation: What would happen if X occurred? (e.g. \"How do you think having 10 hospitals would affect the models?\")\n- Ideation: Generation of ideas without a deliberate end goal (e.g. \"How should the radio look to address the issues?\")- Method: How could an agent accomplish a goal? (e.g. \"How would you measure that?\")\n- Enablement(GD): What object or resource could enable an agent to perform an action? (e.g. \"What system are you going to use to create the UI?\")\nProvide Information:\n-Information: Share related information or examples.\n-Evaluation: Assess the student’s design idea. Stating general facts rather than evaluating a student's ideas doesn't belong.\n-Recommendation: Provide actionable suggestions for improvement.\nSTEP 5: Summarize the extracted knowledge from each category;\nThought Prompting:\n-'Low-Level Question': DO NOT ADD knowledge.\n-'Deep Reasoning Question': Suggest design considerations.\n-'Generate Design Question': Suggest new design opportunities.\nDirect Comments:\n-'Information': Details the provided information.\n-'Evaluation': Describes the assessment of the design.\n-'Recommendation': Outline ideas for enhancement.\nResponse Only in JSON array, which looks like, {\"sentences\":[{”sentence”: “”, “type”:””, “knowledge”:{”knowledge_type”: ””, ”content”: ””}]}.\n-sentence: Individual unit of feedback.\n-type: Subcategory of feedback (e.g., Definition).\n-knowledge: Insights gained from the feedback. If the feedback type is a ‘Deep Reasoning Question’, the ‘knowledge_type’ is ‘Design Consideration’; if it's a ‘Generative Design Question’, it's ‘Design Opportunity’; and otherwise, it's ‘Design Knowledge’.\n-‘content’: Core content of the feedback. Student’s Idea:" + json.dumps(ideasData) + "\nchat Log:" + json.dumps(user_chat.log) + "\nfeedback:" + feedback }]
    student_prompt = [{"role": "system", "content":"This is your design ideas: " + json.dumps(ideasData) + "\nYour knowledge of expanding ideas: " + opportunity + "\nYour knowledge of converging ideas: " + consideration + "\nYour Design knowledge: " + knowledge + "You are a student who is trying to learn design. You're coming up with ideas for a design project. Your persona is \n- a Design Department 1st year student. \n- Korean. (say in Korean) \n- not flexible in design thinking. \n- NEVER apologize, say you can help or just say thanks.\n- NEVER write more than 3 sentences in a single response. Speak colloquially only. Use honorifics.\nAnswer questions from the instructor ONLY based on your knowledge. If you can't answer based on your knowledge, say you don't know. But try to answer AS MUCH AS you can.\nIf " + str(goodQuestionChecker) + ": Mention that was a good question.\nThe format of your answer is JSON as follows. {”answer”: {your answer}}" + "\nThis is previous conversations between you(the student) and the instructor: " + json.dumps(user_chat.log) + "\nThis is the instructor's following chat(feedback): " + feedback }, 
                      {"role": "user", "content":"I am the professor of your class. The class is in the Department of Industrial Design, where you learn about design thinking. I’ll give feedback on your design project."}]

    completion1 = openai.chat.completions.create(
        model="gpt-4o",
        # model="gpt-3.5-turbo",
        messages=feedbackeval_prompt,
        response_format={"type": "json_object"}
    )
    try:
        result1 = json.loads(completion1.choices[0].message.content)
    except ZeroDivisionError as e:
    # This will run only if there is no error
        return {"response": "죄송합니다...제가 잘 이해 못한 거 같아요. 다시 말씀해주실 수 있을까요?"}
    
    new_opportunity = ""
    new_consideration = ""
    new_knowledge = ""
    for sentence in result1["sentences"]:
        print(sentence["knowledge"]["knowledge_type"])
        if sentence["type"] in GoodQuestionCategory:
            goodQuestionChecker = True
        if sentence["knowledge"]["knowledge_type"] == "Design Consideration":
            new_consideration += sentence["knowledge"]["content"]
        if sentence["knowledge"]["knowledge_type"] == "Design Opportunity":
            new_opportunity += sentence["knowledge"]["content"]
        if sentence["knowledge"]["knowledge_type"] == "Design Knowledge":
            new_knowledge += sentence["knowledge"]["content"]
    print("second")
    completion2 = openai.chat.completions.create(
        model="gpt-4o",
        # model="gpt-3.5-turbo",
        messages=student_prompt,
        response_format={"type": "json_object"}
    )
    try:
        result2 = json.loads(completion2.choices[0].message.content)
        print("result2")
    except ZeroDivisionError as e:
    # This will run only if there is no error
        return {"response": "죄송합니다...제가 잘 이해 못한 거 같아요. 다시 말씀해주실 수 있을까요?"}

    user_knowledgestate.opportunity += new_opportunity
    user_knowledgestate.consideration += new_consideration
    user_knowledgestate.knowledge += new_knowledge

    new_entries = [
        {"speaker": "instructor", "content": feedback},
        {"speaker": "student", "content": result2["answer"]}
    ]
    user_chat.log.extend(new_entries)
    flag_modified(user_chat, 'log')
    flag_modified(user_knowledgestate, 'opportunity')
    flag_modified(user_knowledgestate, 'consideration')
    flag_modified(user_knowledgestate, 'knowledge')

    db.session.commit()

    student_divergent_level = len(user_knowledgestate.opportunity)
    student_convergent_level = len(user_knowledgestate.consideration)
    student_knowledge_level = len(user_knowledgestate.knowledge)

    print(student_divergent_level, student_convergent_level, student_knowledge_level)

    return {"response": result2["answer"], "student_divergent_level": student_divergent_level, "student_convergent_level": student_convergent_level, "student_knowledge_level": student_knowledge_level}


# @main.route("/addNote")
# @jwt_required()
# def addNote():
#     user = User.query.filter_by(email=get_jwt_identity()).first()
    
#     new_notes = Note(
#         user_id = user.id,
#         content = "",
#         position = {"x": 0, "y": 0}
#     )
#     db.session.add(new_notes)
#     db.session.commit()

#     notesData = []
#     notes = Note.query.filter_by(user_id=user.id).all()
#     for note in notes:
#         noteData = {"id": note.id, "content": note.content, "position": note.position}
#         notesData.insert(0, noteData)
#     return {"notesData": notesData}


# @main.route("/saveNote", methods=["POST"])
# @cross_origin()
# @jwt_required()
# def saveNote():
#     user = User.query.filter_by(email=get_jwt_identity()).first()
#     params = request.get_json()
#     notesData = params["notesData"]
#     for noteData in notesData:
#         note = Note.query.filter_by(id=noteData['id']).first()
#         note.content = noteData['content']
#         note.position = noteData['position']
#     db.session.commit()
#     return {"msg": "successfully saved!"}


# @main.route("/deleteNote", methods=["POST"])
# @cross_origin()
# @jwt_required()
# def deleteNote():
#     user = User.query.filter_by(email=get_jwt_identity()).first()
#     params = request.get_json()
#     deleteId = params["deleteId"]

#     deletenote = Note.query.filter_by(id=deleteId).first()

#     if deletenote:
#         db.session.delete(deletenote)
#     db.session.commit()

#     notesData = []
#     notes = Note.query.filter_by(user_id=user.id).all()
#     for note in notes:
#         noteData = {"id": note.id, "content": note.content, "position": note.position}
#         notesData.insert(0, noteData)
#     return {"notesData": notesData}



app = create_app()
if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True)