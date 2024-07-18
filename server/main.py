# -*- coding: utf-8 -*-
from flask import Blueprint, current_app, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
from sqlalchemy.orm.attributes import flag_modified
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from __init__ import create_app, db
from models import User, Idea, KnowledgeState, ChatLog, InitialSetting
from datetime import datetime
import base64
import json
import os
import http.client
import openai
import requests

load_dotenv()  # This loads the environment variables from .env

# Now you can access the environment variable
My_OpenAI_key = os.getenv('My_OpenAI_key')
openai.api_key = My_OpenAI_key

LLQ = ["low-level", "verification", "definition", "example", "feature specification", "concept completion", "quantification", "disjunctive", "comparison", "judgmental"]
DRQ = ["deep reasoning", "interpretation", "goal orientation", "causal antecedent", "causal consequent", "expectational", "instrumental/procedural", "instrumental", "procedural", "enablement(dr)"]
GDQ = ["generate design", "proposal/negotiation", "proposal", "negotiation", "scenario creation", "ideation", "method", "enablement(gd)"]

IdeaCategory = ['product', 'uiux', 'public']

Ideas = [
    {'title': "product유아친화 지역 사회 공간", 'target_problem': "아이를 키우는 환경의 부족", 'idea': "지역 사회 내에서 안전하고 창의적인 유아친화 공간을 만들어 부모들이 아이들을 더욱 편리하고 즐겁게 키울 수 있도록 지원합니다. 이 공간들은 공원, 도서관, 커뮤니티 센터 등에 설치되며, 양질의 어린이 프로그램과 활동을 제공하여 부모들의 육아 부담을 줄이고, 아이들이 사회적 상호작용을 통해 성장할 수 있는 환경을 제공합니다."},
    {'title': "product플렉스 워크 포인트", 'target_problem': "일과 가정의 균형 부족", 'idea': "기업들이 육아와 일을 병행할 수 있도록 유연한 근무 환경을 제공하는 정책을 도입합니다. 이 아이디어는 육아 휴직, 시간 선택 근무, 재택 근무 옵션을 포함하여 부모가 자녀 양육에 더 많은 시간을 할애할 수 있게 돕습니다. 또한, 직장 내 어린이집을 설치하여 부모가 직장 근처에서 아이들과 더 많은 시간을 보낼 수 있게 합니다."},
    {'title': "product노인과 청년 연결 프로그램", 'target_problem': "고령화 사회의 노인 인력 활용", 'idea': "노인 세대가 자신의 지식과 경험을 청년 세대에게 전달할 수 있는 멘토링 및 지원 프로그램을 개발합니다. 이 프로그램은 노인을 일자리와 연결하여 활동적인 사회 생활을 유지하게 돕고, 동시에 젊은 부모나 예비 부모에게 육아와 관련된 지식과 지원을 제공합니다. 이러한 상호작용은 세대 간의 소통과 이해를 증진시키고, 고령화 사회에서의 노인들의 역할을 재정의합니다."},
    {'title': "uiux유아친화 지역 사회 공간", 'target_problem': "아이를 키우는 환경의 부족", 'idea': "지역 사회 내에서 안전하고 창의적인 유아친화 공간을 만들어 부모들이 아이들을 더욱 편리하고 즐겁게 키울 수 있도록 지원합니다. 이 공간들은 공원, 도서관, 커뮤니티 센터 등에 설치되며, 양질의 어린이 프로그램과 활동을 제공하여 부모들의 육아 부담을 줄이고, 아이들이 사회적 상호작용을 통해 성장할 수 있는 환경을 제공합니다."},
    {'title': "uiux플렉스 워크 포인트", 'target_problem': "일과 가정의 균형 부족", 'idea': "기업들이 육아와 일을 병행할 수 있도록 유연한 근무 환경을 제공하는 정책을 도입합니다. 이 아이디어는 육아 휴직, 시간 선택 근무, 재택 근무 옵션을 포함하여 부모가 자녀 양육에 더 많은 시간을 할애할 수 있게 돕습니다. 또한, 직장 내 어린이집을 설치하여 부모가 직장 근처에서 아이들과 더 많은 시간을 보낼 수 있게 합니다."},
    {'title': "uiux노인과 청년 연결 프로그램", 'target_problem': "고령화 사회의 노인 인력 활용", 'idea': "노인 세대가 자신의 지식과 경험을 청년 세대에게 전달할 수 있는 멘토링 및 지원 프로그램을 개발합니다. 이 프로그램은 노인을 일자리와 연결하여 활동적인 사회 생활을 유지하게 돕고, 동시에 젊은 부모나 예비 부모에게 육아와 관련된 지식과 지원을 제공합니다. 이러한 상호작용은 세대 간의 소통과 이해를 증진시키고, 고령화 사회에서의 노인들의 역할을 재정의합니다."},
    {'title': "uiux유아친화 지역 사회 공간", 'target_problem': "아이를 키우는 환경의 부족", 'idea': "지역 사회 내에서 안전하고 창의적인 유아친화 공간을 만들어 부모들이 아이들을 더욱 편리하고 즐겁게 키울 수 있도록 지원합니다. 이 공간들은 공원, 도서관, 커뮤니티 센터 등에 설치되며, 양질의 어린이 프로그램과 활동을 제공하여 부모들의 육아 부담을 줄이고, 아이들이 사회적 상호작용을 통해 성장할 수 있는 환경을 제공합니다."},
    {'title': "uiux플렉스 워크 포인트", 'target_problem': "일과 가정의 균형 부족", 'idea': "기업들이 육아와 일을 병행할 수 있도록 유연한 근무 환경을 제공하는 정책을 도입합니다. 이 아이디어는 육아 휴직, 시간 선택 근무, 재택 근무 옵션을 포함하여 부모가 자녀 양육에 더 많은 시간을 할애할 수 있게 돕습니다. 또한, 직장 내 어린이집을 설치하여 부모가 직장 근처에서 아이들과 더 많은 시간을 보낼 수 있게 합니다."},
    {'title': "uiux노인과 청년 연결 프로그램", 'target_problem': "고령화 사회의 노인 인력 활용", 'idea': "노인 세대가 자신의 지식과 경험을 청년 세대에게 전달할 수 있는 멘토링 및 지원 프로그램을 개발합니다. 이 프로그램은 노인을 일자리와 연결하여 활동적인 사회 생활을 유지하게 돕고, 동시에 젊은 부모나 예비 부모에게 육아와 관련된 지식과 지원을 제공합니다. 이러한 상호작용은 세대 간의 소통과 이해를 증진시키고, 고령화 사회에서의 노인들의 역할을 재정의합니다."}
]

ideaOrder = [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]


def flag_all_modified(instance):
    for attr in instance.__mapper__.attrs.keys():
        flag_modified(instance, attr)

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
        realPassword = password,
        currentRound = 1
    )
    db.session.add(new_user)
    db.session.commit()

    new_KnowledgeStates = [
        KnowledgeState(user_id = new_user.id, round=1, face=33, q_num=0, s_num=0, qns=0, cnd=0, eval={'uniqueness': 0, 'relevance': 0, 'high-level': 0, 'specificity': 0, 'justification': 0, 'active': 0}, knowledge = "", counter={'q_count': 0, 'd_count': 0, 'u_count': 0, 'r_count': 0, 'h_count': 0, 's_count': 0, 'j_count': 0, 'a_count': 0}),
        KnowledgeState(user_id = new_user.id, round=2, face=33, q_num=0, s_num=0, qns=0, cnd=0, eval={'uniqueness': 0, 'relevance': 0, 'high-level': 0, 'specificity': 0, 'justification': 0, 'active': 0}, knowledge = "", counter={'q_count': 0, 'd_count': 0, 'u_count': 0, 'r_count': 0, 'h_count': 0, 's_count': 0, 'j_count': 0, 'a_count': 0}),
        KnowledgeState(user_id = new_user.id, round=3, face=33, q_num=0, s_num=0, qns=0, cnd=0, eval={'uniqueness': 0, 'relevance': 0, 'high-level': 0, 'specificity': 0, 'justification': 0, 'active': 0}, knowledge = "", counter={'q_count': 0, 'd_count': 0, 'u_count': 0, 'r_count': 0, 'h_count': 0, 's_count': 0, 'j_count': 0, 'a_count': 0})
    ]

    new_ChatLogs = [
        ChatLog(user_id = new_user.id, round=1, log = [{"speaker":"student", "content": "안녕하세요! 저는 동건이라고 합니다. 제가 " + IdeaCategory[ideaOrder[new_user.id % 3][0]] + " 디자인과 관련하여 세가지 아이디어를 생각해보았는데요. 보시고 피드백을 주시면 감사하겠습니다."}]),
        ChatLog(user_id = new_user.id, round=2, log = [{"speaker":"student", "content": "안녕하세요! 저는 동건이라고 합니다. 제가 " + IdeaCategory[ideaOrder[new_user.id % 3][1]]  + " 디자인과 관련하여 세가지 아이디어를 생각해보았는데요. 보시고 피드백을 주시면 감사하겠습니다."}]),
        ChatLog(user_id = new_user.id, round=3, log = [{"speaker":"student", "content": "안녕하세요! 저는 동건이라고 합니다. 제가 " + IdeaCategory[ideaOrder[new_user.id % 3][2]]  + " 디자인과 관련하여 세가지 아이디어를 생각해보았는데요. 보시고 피드백을 주시면 감사하겠습니다."}])
    ]

    new_ideas = [
        Idea(user_id=new_user.id, round=1, title=Ideas[ideaOrder[new_user.id % 3][0] * 3]['title'], target_problem=Ideas[ideaOrder[new_user.id % 3][0] * 3]['target_problem'], idea=Ideas[ideaOrder[new_user.id % 3][0] * 3]['idea']),
        # Idea(user_id=new_user.id, round=1, title=Ideas[ideaOrder[new_user.id % 3][0] * 3 + 1]['title'], target_problem=Ideas[ideaOrder[new_user.id % 3][0] * 3 + 1]['target_problem'], idea=Ideas[ideaOrder[new_user.id % 3][0] * 3 + 1]['idea']),
        # Idea(user_id=new_user.id, round=1, title=Ideas[ideaOrder[new_user.id % 3][0] * 3 + 2]['title'], target_problem=Ideas[ideaOrder[new_user.id % 3][0] * 3 + 2]['target_problem'], idea=Ideas[ideaOrder[new_user.id % 3][0] * 3 + 2]['idea']),
        Idea(user_id=new_user.id, round=2, title=Ideas[ideaOrder[new_user.id % 3][1] * 3]['title'], target_problem=Ideas[ideaOrder[new_user.id % 3][1] * 3]['target_problem'], idea=Ideas[ideaOrder[new_user.id % 3][1] * 3]['idea']),
        # Idea(user_id=new_user.id, round=2, title=Ideas[ideaOrder[new_user.id % 3][1] * 3 + 1]['title'], target_problem=Ideas[ideaOrder[new_user.id % 3][1] * 3 + 1]['target_problem'], idea=Ideas[ideaOrder[new_user.id % 3][1] * 3 + 1]['idea']),
        # Idea(user_id=new_user.id, round=2, title=Ideas[ideaOrder[new_user.id % 3][1] * 3 + 2]['title'], target_problem=Ideas[ideaOrder[new_user.id % 3][1] * 3 + 2]['target_problem'], idea=Ideas[ideaOrder[new_user.id % 3][1] * 3 + 2]['idea']),
        Idea(user_id=new_user.id, round=3, title=Ideas[ideaOrder[new_user.id % 3][2] * 3]['title'], target_problem=Ideas[ideaOrder[new_user.id % 3][2] * 3]['target_problem'], idea=Ideas[ideaOrder[new_user.id % 3][2] * 3]['idea']),
        # Idea(user_id=new_user.id, round=3, title=Ideas[ideaOrder[new_user.id % 3][2] * 3 + 1]['title'], target_problem=Ideas[ideaOrder[new_user.id % 3][2] * 3 + 1]['target_problem'], idea=Ideas[ideaOrder[new_user.id % 3][2] * 3 + 1]['idea']),
        # Idea(user_id=new_user.id, round=3, title=Ideas[ideaOrder[new_user.id % 3][2] * 3 + 2]['title'], target_problem=Ideas[ideaOrder[new_user.id % 3][2] * 3 + 2]['target_problem'], idea=Ideas[ideaOrder[new_user.id % 3][2] * 3 + 2]['idea'])
        # Idea(user_id=new_user.id, title="유아친화 지역 사회 공간", target_problem="아이를 키우는 환경의 부족", idea="지역 사회 내에서 안전하고 창의적인 유아친화 공간을 만들어 부모들이 아이들을 더욱 편리하고 즐겁게 키울 수 있도록 지원합니다. 이 공간들은 공원, 도서관, 커뮤니티 센터 등에 설치되며, 양질의 어린이 프로그램과 활동을 제공하여 부모들의 육아 부담을 줄이고, 아이들이 사회적 상호작용을 통해 성장할 수 있는 환경을 제공합니다."),
        # Idea(user_id=new_user.id, title="플렉스 워크 포인트", target_problem="일과 가정의 균형 부족", idea="기업들이 육아와 일을 병행할 수 있도록 유연한 근무 환경을 제공하는 정책을 도입합니다. 이 아이디어는 육아 휴직, 시간 선택 근무, 재택 근무 옵션을 포함하여 부모가 자녀 양육에 더 많은 시간을 할애할 수 있게 돕습니다. 또한, 직장 내 어린이집을 설치하여 부모가 직장 근처에서 아이들과 더 많은 시간을 보낼 수 있게 합니다."),
        # Idea(user_id=new_user.id, title="노인과 청년 연결 프로그램", target_problem="고령화 사회의 노인 인력 활용", idea="노인 세대가 자신의 지식과 경험을 청년 세대에게 전달할 수 있는 멘토링 및 지원 프로그램을 개발합니다. 이 프로그램은 노인을 일자리와 연결하여 활동적인 사회 생활을 유지하게 돕고, 동시에 젊은 부모나 예비 부모에게 육아와 관련된 지식과 지원을 제공합니다. 이러한 상호작용은 세대 간의 소통과 이해를 증진시키고, 고령화 사회에서의 노인들의 역할을 재정의합니다.")
        # Idea(user_id=new_user.id, title="인공지능 에이전트를 활용한 한글 회화 서비스", target_problem="한글을 배우고 싶어하는 외국인들이 대화를 연습해볼 상대를 찾기 어려움", idea="이 서비스는 대규모 언어모델을 기반으로 하는 인공지능 에이전트를 활용하여 한글을 배우고자 하는 외국인 사용자들에게 실시간 대화 연습 기회를 제공합니다. 사용자의 언어 수준과 관심사에 맞춰 개인화된 대화가 가능하며, 다양한 주제와 상황에 맞는 대화 시나리오를 제공하여 실제와 같은 대화 환경을 조성합니다. 또한, 사용자의 발음, 문법, 어휘 사용 등을 분석하여 즉각적인 피드백과 개선 방향을 제시함으로써 효율적인 학습이 가능하도록 돕습니다."),
        # Idea(user_id=new_user.id, title="신뢰도 있는 공동창업자 구인 시스템", target_problem="기존 커뮤니티는 개인정보가 보장되지 않아 믿을만한 공동창업자를 찾기 어려움", idea="이 서비스는 사용자(구직자)의 경력, 학력, 그리고 능력을 면밀히 검증하고 이를 보장하는 방식의 공동창업자 구인 시스템입니다. 서비스 제공자는 각 후보의 제출 자료를 AI 기반의 분석 도구를 사용하여 검증하고, 이 정보를 기반으로 신뢰도 높은 프로필을 생성합니다. 이렇게 검증된 프로필을 바탕으로, 사용자는 자신과 가장 잘 맞는 공동창업자를 찾을 수 있으며, AI는 사용자의 선호도와 요구 사항에 따라 최적의 매칭을 제안합니다. 이 시스템은 창업 과정에서 중요한 신뢰성과 투명성을 제공하여 안전한 창업 파트너십을 가능하게 합니다."),
        # Idea(user_id=new_user.id, title="개인화된 사무용 인공지능 비서", target_problem="기존 사무용 인공지능 비서는 개인의 업무에 특화되어 있지 않아 업무에 활용하기 어려움", idea="이 서비스는 대규모 언어모델을 활용하여 각 사용자의 업무 스타일과 선호도에 맞춤화된 개인 사무용 인공지능 비서를 제공합니다. 이 AI 비서는 사용자의 업무 패턴, 선호하는 커뮤니케이션 방식, 그리고 반복되는 업무를 학습하여, 시간 관리, 이메일 자동화, 문서 작성 및 관리 등의 업무를 개인화하여 지원합니다. 또한, 실시간으로 업무 진행 상황을 분석하고 조정할 수 있는 도구를 제공하여, 사용자가 보다 효율적으로 업무를 수행할 수 있도록 돕습니다. 이러한 개인화된 지원은 사용자의 업무 효율을 대폭 향상시킬 것입니다.")
    ]

    db.session.add_all(new_ideas)
    db.session.add_all(new_KnowledgeStates)
    db.session.add_all(new_ChatLogs)
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
    ideas = Idea.query.filter_by(user_id=user.id, round=user.currentRound).all()
    ideasData = [{"id": idea.id, "title": idea.title, "problem": idea.target_problem, "idea": idea.idea} for idea in ideas]
    userChat = ChatLog.query.filter_by(user_id=user.id, round=user.currentRound).first()
    setting = InitialSetting.query.filter_by(user_id=user.id, round=user.currentRound).first()
    user_knowledgestate = KnowledgeState.query.filter_by(user_id=user.id, round=user.currentRound).first()
    
    feedback_uniqueness = 0
    feedback_relevance = 0
    feedback_high_level = 0
    feedback_specificity = 0
    feedback_justification = 0
    feedback_active = 0
    if user_knowledgestate.q_num > 0:
        feedback_uniqueness = round(user_knowledgestate.eval['uniqueness'] / user_knowledgestate.q_num, 1)
        feedback_relevance = round(user_knowledgestate.eval['relevance'] / user_knowledgestate.q_num, 1)
        feedback_high_level = round(user_knowledgestate.eval['high-level'] / user_knowledgestate.q_num, 1)
    if user_knowledgestate.s_num > 0:
        feedback_specificity = round(user_knowledgestate.eval['specificity'] / user_knowledgestate.s_num, 1)
        feedback_justification = round(user_knowledgestate.eval['justification'] / user_knowledgestate.s_num, 1)
        feedback_active = round(user_knowledgestate.eval['active'] / user_knowledgestate.s_num, 1)

    return {"ideasData": ideasData, "chatData": userChat.log, "name": name, "mode": user.mode, "character": setting.character, "goal1": setting.goal1, "goal2": setting.goal2, "goal3": setting.goal3, "time": setting.time, "student_knowledge_level": len(user_knowledgestate.knowledge), "qns": user_knowledgestate.qns, "cnd": user_knowledgestate.cnd, "uniqueness": feedback_uniqueness, "relevance": feedback_relevance, "high_level": feedback_high_level, "specificity": feedback_specificity, "justification": feedback_justification, "active": feedback_active, 'face': user_knowledgestate.face}

@main.route("/mode", methods=["POST"])
@jwt_required()
@cross_origin()
def mode():
    params = request.get_json()
    user_mode = params['mode']
    user = User.query.filter_by(email=get_jwt_identity()).first()
    
    user.mode = user_mode
    new_settings = [
        InitialSetting(user_id=user.id, round=1, character = 0, goal1="", goal2="", goal3="", time = 20),
        InitialSetting(user_id=user.id, round=2, character = 0, goal1="", goal2="", goal3="", time = 20),
        InitialSetting(user_id=user.id, round=3, character = 0, goal1="", goal2="", goal3="", time = 20)
    ]

    flag_modified(user, 'mode')
    db.session.add_all(new_settings)
    db.session.commit()

    return {"msg": "select mode"}

@main.route("/getSetting")
@jwt_required()
@cross_origin()
def getSetting():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    currentRound = user.currentRound
    if currentRound >= 4:
        return {"msg": "Done!"}
    setting = InitialSetting.query.filter_by(user_id=user.id, round=currentRound).first()
    return {"order": (user.id % 6), "mode": user.mode, "round": currentRound, "character": setting.character, "goal1": setting.goal1, "goal2": setting.goal2, "goal3": setting.goal3, "time": setting.time}

@main.route("/saveSetting", methods=["POST"])
@jwt_required()
@cross_origin()
def saveSetting():
    params = request.get_json()
    current_character = params['character']
    current_goal1 = params['goal1']
    current_goal2 = params['goal2']
    current_goal3 = params['goal3']
    current_time = params['time']
    user = User.query.filter_by(email=get_jwt_identity()).first()
    currentRound = user.currentRound

    if currentRound <= 1:
        setting1 = InitialSetting.query.filter_by(user_id=user.id, round=1).first()
        setting1.character = current_character
        setting1.goal1 = current_goal1
        setting1.goal2 = current_goal2
        setting1.goal3 = current_goal3
        setting1.time = current_time
        flag_all_modified(setting1)

    if currentRound <=2:
        setting2 = InitialSetting.query.filter_by(user_id=user.id, round=2).first()
        setting2.character = current_character
        setting2.goal1 = current_goal1
        setting2.goal2 = current_goal2
        setting2.goal3 = current_goal3
        setting2.time = current_time
        flag_all_modified(setting2)

    if currentRound <=3:        
        setting3 = InitialSetting.query.filter_by(user_id=user.id, round=3).first()
        setting3.character = current_character
        setting3.goal1 = current_goal1
        setting3.goal2 = current_goal2
        setting3.goal3 = current_goal3
        setting3.time = current_time
        flag_all_modified(setting3)
    
    db.session.commit()
    return {"msg": "save the current setting"}

@main.route("/response", methods=["POST"])
@jwt_required()
@cross_origin()
def response():
    params = request.get_json()
    feedback = params['feedback']
    user = User.query.filter_by(email=get_jwt_identity()).first()
    ideasData = []
    ideas = Idea.query.filter_by(user_id=user.id, round=user.currentRound).all()
    ideasData = [{"id": idea.id, "title": idea.title, "problem": idea.target_problem, "idea": idea.idea} for idea in ideas]
    user_knowledgestate = KnowledgeState.query.filter_by(user_id=user.id, round=user.currentRound).first()
    # opportunity = user_knowledgestate.opportunity
    # consideration = user_knowledgestate.consideration
    knowledge = user_knowledgestate.knowledge
    user_chat = ChatLog.query.filter_by(user_id=user.id, round=user.currentRound).first()

    feedbackcate_prompt = [{"role": "system", "content":"Feedback Analysis Instructions for Instructor's Feedback of a Student's Design Idea.\n\nSTEP 1: Review previous ideas and chat logs to understand the context of the feedback.\n\nSTEP 2: Decompose the feedback into individual sentences.\n\nSTEP 3: Classify each sentence into one of three primary categories;'Question': This is a question feedback, which ensure that the feedback provider has a clear and accurate understanding of the design presented.;'Statement': This is a statement feedback, which provides relevant information or is directly related to a design idea to evaluate or suggest improvements.;'No feedback': This sentence is completely irrelevant to the feedback.\n\nSTEP 4: Subcategorize each sentence based on its nature (There are 21 types of 'Question', three types of 'Statement' and no sub category for 'No feedback.'); 'Question':\n\"Low-Level\": Seeks factual details about the design.\n- Verification: Is X true?\n- Definition: What does X mean?\n- Example: What is an example of X?\n- Feature Specification: What (qualitative) attributes does X have?\n- Concept Completion: Who? What? When? Where?\n- Quantification: How much? How many?\n- Disjunctive: Is X or Y the case?\n- Comparison: How does X compare to Y?\n- Judgmental: What is your opinion on X?\n\"Deep Reasoning\": Explores deeper implications or reasons behind the design.\n- Interpretation: How is a particular event or pattern of information interpreted or summarized?\n- Goal Orientation: What are the motives behind an agent’s action?\n- Causal Antecedent: What caused X to occur?\n- Causal Consequent: What were the consequences of X occurring?\n- Expectational: Why is X not true?\n- Instrumental/Procedural: How does an agent accomplish a goal?\n- Enablement(DR): What object or resource enables an agent to perform an action?\n\"Generate Design\": Encourages innovative thinking about design challenges.\n- Proposal/Negotiation: Could a new concept be suggested/negotiated?\n- Scenario Creation: What would happen if X occurred?\n- Ideation: Generation of ideas without a deliberate end goal\n- Method: How could an agent accomplish a goal?\n- Enablement(GD): What object or resource could enable an agent to perform an action?\n'Statement':\n\"Information\": Share related information or examples.\n\"Evaluation\": Assess the student’s design idea. Stating general facts rather than evaluating a student's ideas doesn't belong.\n\"Recommendation\": Provide actionable suggestions for improvement.\n\nSTEP 5: Summarize the extracted knowledge from each category. Knowledge includes only key approaches and keywords and excludes complex context.\n'Question':\n\"Low-Level\": DO NOT ADD knowledge.\n\"Deep Reasoning\": Suggest design considerations.\n\"Generate Design\": Suggest new design opportunities.\n'Statement':\n\"Information\": Details the provided information.\n\"Evaluation\": Describes the assessment of the design.\n\"Recommendation\": Outline ideas for enhancement.\n'No feedback': DO NOT ADD knowledge.\n\nSTEP 6: Check whether the knowledge is already known to the student or not.\n\nResponse Only in JSON array, which looks like, {\"sentences\":[{\"sentence\": \"\", \"categories\":\"\", \"type\":\"\", \"knowledge\":\"\", \"isNew\":\"\"}]}.\n\"sentence\": Individual unit of feedback.\n\"categories\": Category of feedback. ('Question' or 'Statement' or 'No feedback')\n\"type\": Subcategory of feedback (e.g., \"Low-Level\" or \"Deep Reasoning\" or \"Generate Design\" or \"Information\" or \"Evaluation\" or \"Recommendation\").\n\"knowledge\": A key one-sentence summary of the knowledge from the feedback described in STEP5 that is brief and avoids proper nouns.\n\"isNew\": If it's new knowledge, true; otherwise, false.\nStudent's Idea:" + json.dumps(ideasData) + "\nStudent's Knowledge:" + knowledge + "\nchat Log:" + json.dumps(user_chat.log) + "\nfeedback:" + feedback}]
    student_prompt = [{"role": "system", "content":"This is your design ideas: " + json.dumps(ideasData) + "\nYour Design Knowledge: " + knowledge + "\nYou are a student who is trying to learn design. You're coming up with ideas for a design project. Your persona is \n* A Design Department 1st year student. \n* Korean. (say in Korean) \n* NEVER apologize, NEVER say you can help, and NEVER just say thanks.\n* NEVER write more than 3 sentences in a single response. Speak colloquially only. Use honorifics.\n\nAnswer questions from the feedback provider ONLY based on your knowledge. If you can't answer based on Your Design Knowledge, say you don't know. BUT try to answer AS MUCH AS you can.\n\nThe format of your answer is JSON as follows. {\"answer\": {your answer}}\nThis is previous conversations between you(the student) and the feedback provider: " + json.dumps(user_chat.log) + "\nThis is the feedback provider's following chat(feedback): " + feedback}, 
                      {"role": "user", "content":"I am an industrial design expert. As a mento, I'll give feedback on your design project."}]

    completion1 = openai.chat.completions.create(
        model="gpt-4o",
        # model="gpt-3.5-turbo",
        temperature=0,
        messages=feedbackcate_prompt,
        response_format={"type": "json_object"}
    )
    try:
        result1 = json.loads(completion1.choices[0].message.content)
        result1 = [sentence for sentence in result1['sentences'] if sentence['categories'].lower() in ['question', 'statement']]
    except ZeroDivisionError as e:
        # This will run only if there is no error
        return {"response": "죄송합니다...제가 잘 이해 못한 거 같아요. 다시 말씀해주실 수 있을까요?"}

    feedbackeval_prompt = [{"role": "system", "content":"Feedback Evaluation Instructions for Instructor's Feedback of a Student's Design Idea.\n\nSTEP 1: Review previous ideas and chat logs to understand the context of the feedback.\n\nSTEP 2: Evaluate the feedback on a scale of 1 to 57 based on the following criteria. There are three different criteria depending on whether the feedback category is a 'Question' or a 'Statement'.\n'Question':\n\"uniqueness\": The question is unique.\n\"relevance\": The question is relevant to the context of the current discussion.\n\"high-level\": The question is high-level.(If the question falls into the \"Low-Level\" category, it's between 1 and 2. Otherwise, it's between 3 and 5.)\n'Statement':\n\"specificity\": The feedback is specific.\n\"justification\": The feedback is justified.\n\"active\": The feedback is actionable\n'No feedback': DO NOT RATE.\nSTEP 3: Evaluate the sentiment of the feedback. Analyze the sentiment of the feedback and rate it as either positive(1), neutral(0), or negative(-1).\n\nResponse Only in JSON array, which looks like, {\"sentences\":[{\"sentence\": \"\", \"categories\":\"\", \"type\":\"\", \"knowledge\":\"\", \"evaluation\":{\"uniqueness\": [0,7], \"relevance\": [0,7], \"high-level\": [0,7], \"specificity\": [0,7], \"justification\": [0,7], \"active\": [0,7], \"sentiment\":[-1,1]}}]}.\n\"sentence\": Individual unit of feedback.\n\"categories\": Category of feedback. ('Question' or 'Statement' or 'No feedback')\n\"type\": Subcategory of feedback (e.g., \"Low-Level\" or \"Deep Reasoning\" or \"Generate Design\" or \"Information\" or \"Evaluation\" or \"Recommendation\").\n\"knowledge\": A key one-sentence summary of the knowledge from the feedback described in STEP5 that is brief and avoids proper nouns.\n\"evaluation\": JSON with the evaluation score based on the criteria. The criteria that should be evaluated in STEP 2 have a value between 1-7, with the rest evaluated as 0.\n\nStudent's Idea:" + json.dumps(ideasData) + "\nchat Log:" + json.dumps(user_chat.log) + "\nfeedback:" + str(result1)}]

    # Add Knowledge
    new_knowledge = ""
    for sentence in result1:
        try:
            if sentence['isNew']:
                new_knowledge += sentence["knowledge"]
        except:
            return {"response": "죄송합니다...제가 잘 이해 못한 거 같아요. 다시 말씀해주실 수 있을까요?"}
    user_knowledgestate.knowledge += new_knowledge

    if len(result1) == 0:
        if (user_knowledgestate.face / 10) > 1:
            print('hi')
            user_knowledgestate.face -= 10

    else:
        # Second Prompt for Evaluate feedback
        completion2 = openai.chat.completions.create(
            model="gpt-4o",
            # model="gpt-3.5-turbo",
            messages=feedbackeval_prompt,
            temperature=0,
            response_format={"type": "json_object"}
        )
        try:
            result2 = json.loads(completion2.choices[0].message.content)
            print(result2)
        except ZeroDivisionError as e:
            # This will run only if there is no error
            return {"response": "죄송합니다...제가 잘 이해 못한 거 같아요. 다시 말씀해주실 수 있을까요?"}

        sentiment_counter = 0
        
        for sentence in result2["sentences"]:
            try:
                if sentence['type'].lower() in LLQ + DRQ + GDQ:
                    user_knowledgestate.counter['q_count'] += 1
                    user_knowledgestate.q_num += 1
                    if user_knowledgestate.qns > -5:
                        user_knowledgestate.qns -= 1
                    #uniqueness
                    user_knowledgestate.eval['uniqueness'] += int(sentence['evaluation']['uniqueness'])
                    if sentence['evaluation']['uniqueness'] <= 4:
                        user_knowledgestate.counter['u_count'] += 1
                    #relevance
                    user_knowledgestate.eval['relevance'] += int(sentence['evaluation']['relevance'])
                    if sentence['evaluation']['relevance'] <= 4:
                        user_knowledgestate.counter['r_count'] += 1
                    #high-level
                    user_knowledgestate.eval['high-level'] += int(sentence['evaluation']['high-level'])
                    if sentence['evaluation']['high-level'] <= 4:
                        user_knowledgestate.counter['h_count'] += 1

                    if (int(sentence['evaluation']['uniqueness']) + int(sentence['evaluation']['relevance']) + int(sentence['evaluation']['high-level']) >= 15) and ((user_knowledgestate.face / 10) < 5):
                        print(user_knowledgestate.face / 10)
                        user_knowledgestate.face += 10
                    elif (int(sentence['evaluation']['uniqueness']) + int(sentence['evaluation']['relevance']) + int(sentence['evaluation']['high-level']) <= 9) and ((user_knowledgestate.face / 10) > 1):
                        print(user_knowledgestate.face / 10)
                        user_knowledgestate.face -= 10

                    flag_modified(user_knowledgestate, 'counter')
                    flag_modified(user_knowledgestate, 'q_num')
                    flag_modified(user_knowledgestate, 'qns')
                    flag_modified(user_knowledgestate, 'eval')
    
                if sentence['type'].lower() in ['information', 'evalutation', 'recommendation']:
                    user_knowledgestate.counter['q_count'] -= 1
                    user_knowledgestate.s_num += 1
                    if user_knowledgestate.qns < 5:
                        user_knowledgestate.qns += 1
                    #specificity
                    user_knowledgestate.eval['specificity'] += int(sentence['evaluation']['specificity'])
                    if sentence['evaluation']['specificity'] <= 4:
                        user_knowledgestate.counter['s_count'] += 1
                    #justification
                    user_knowledgestate.eval['justification'] += int(sentence['evaluation']['justification'])
                    if sentence['evaluation']['justification'] <= 4:
                        user_knowledgestate.counter['j_count'] += 1
                    #active
                    user_knowledgestate.eval['active'] += int(sentence['evaluation']['active'])
                    if sentence['evaluation']['active'] <= 4:
                        user_knowledgestate.counter['a_count'] += 1

                    if (int(sentence['evaluation']['specificity']) + int(sentence['evaluation']['justification']) + int(sentence['evaluation']['active']) >= 15) and ((user_knowledgestate.face / 10) < 5):
                        user_knowledgestate.face += 10
                    elif (int(sentence['evaluation']['specificity']) + int(sentence['evaluation']['justification']) + int(sentence['evaluation']['active']) <= 9) and ((user_knowledgestate.face / 10) > 1):
                        user_knowledgestate.face -= 10

                    flag_modified(user_knowledgestate, 'counter')
                    flag_modified(user_knowledgestate, 's_num')
                    flag_modified(user_knowledgestate, 'qns')
                    flag_modified(user_knowledgestate, 'eval')

                if sentence['type'].lower() in GDQ + ['recommendation']:
                    user_knowledgestate.counter['d_count'] += 1
                    if user_knowledgestate.cnd < 5:
                        user_knowledgestate.cnd += 1
                        flag_modified(user_knowledgestate, 'cnd')
                    flag_modified(user_knowledgestate, 'counter')

                if sentence['type'].lower() in DRQ + ['evaluation']:
                    user_knowledgestate.counter['d_count'] -= 1
                    if user_knowledgestate.cnd > -5:
                        user_knowledgestate.cnd -= 1
                        flag_modified(user_knowledgestate, 'cnd')
                    flag_modified(user_knowledgestate, 'counter')
                
                sentiment_counter += sentence['evaluation']['sentiment']
                
                flag_modified(user_knowledgestate, 'face')

            except:
                return {"response": "죄송합니다...제가 잘 이해 못한 거 같아요. 다시 말씀해주실 수 있을까요?"}
            
        if ((user_knowledgestate.face % 10) < 5) and (sentiment_counter > 0):
            user_knowledgestate.face += 1
        elif ((user_knowledgestate.face % 10) > 1) and (sentiment_counter < 0):
            user_knowledgestate.face -= 1
            
    completion3 = openai.chat.completions.create(
        model="gpt-4o",
        # model="gpt-3.5-turbo",
        messages=student_prompt,
        response_format={"type": "json_object"}
    )
    try:
        result3 = json.loads(completion3.choices[0].message.content)
    except ZeroDivisionError as e:
    # This will run only if there is no error
        return {"response": "죄송합니다...제가 잘 이해 못한 거 같아요. 다시 말씀해주실 수 있을까요?"}

    new_entries = [
        {"speaker": "instructor", "content": feedback},
        {"speaker": "student", "content": result3["answer"]}
    ]
    user_chat.log.extend(new_entries)
    flag_modified(user_chat, 'log')
    flag_modified(user_knowledgestate, 'knowledge')

    db.session.commit()

    # student_divergent_level = len(user_knowledgestate.opportunity)
    # student_convergent_level = len(user_knowledgestate.consideration)
    student_knowledge_level = len(user_knowledgestate.knowledge)
    feedback_uniqueness = 0
    feedback_relevance = 0
    feedback_high_level = 0
    feedback_specificity = 0
    feedback_justification = 0
    feedback_active = 0
    if user_knowledgestate.q_num > 0:
        feedback_uniqueness = round(user_knowledgestate.eval['uniqueness'] / user_knowledgestate.q_num, 1)
        feedback_relevance = round(user_knowledgestate.eval['relevance'] / user_knowledgestate.q_num, 1)
        feedback_high_level = round(user_knowledgestate.eval['high-level'] / user_knowledgestate.q_num, 1)
    if user_knowledgestate.s_num > 0:
        feedback_specificity = round(user_knowledgestate.eval['specificity'] / user_knowledgestate.s_num, 1)
        feedback_justification = round(user_knowledgestate.eval['justification'] / user_knowledgestate.s_num, 1)
        feedback_active = round(user_knowledgestate.eval['active'] / user_knowledgestate.s_num, 1)
    
    question_checker = not (
        (user_knowledgestate.counter['q_count'] < 3)
        and (user_knowledgestate.counter['q_count'] > -3)
        and (user_knowledgestate.counter['d_count'] < 3) 
        and (user_knowledgestate.counter['d_count'] > -3) 
        and (user_knowledgestate.counter['u_count'] < 3) 
        and (user_knowledgestate.counter['r_count'] < 3) 
        and (user_knowledgestate.counter['h_count'] < 3)
        and (user_knowledgestate.counter['s_count'] < 3)
        and (user_knowledgestate.counter['j_count'] < 3)
        and (user_knowledgestate.counter['a_count'] < 3)
    )

    # print(feedback_uniqueness)
    # print(feedback_relevance)
    # print(feedback_high_level)
    # print(feedback_specificity)
    # print(feedback_justification)
    # print(feedback_active)
    # print(user_knowledgestate.qns)

    # print("opportunity: ", user_knowledgestate.opportunity)
    # print("consideration: ", user_knowledgestate.consideration)
    # print(question_checker)
    # print(user_knowledgestate.face)
    # print("knowledge: ", user_knowledgestate.knowledge)

    return {"response": result3["answer"], "student_knowledge_level": student_knowledge_level, "qns": user_knowledgestate.qns, "cnd": user_knowledgestate.cnd, "uniqueness": feedback_uniqueness, "relevance": feedback_relevance, "high_level": feedback_high_level, "specificity": feedback_specificity, "justification": feedback_justification, "active": feedback_active, "questionChecker": question_checker, "face": user_knowledgestate.face}

@main.route("/askQuestion")
@jwt_required()
@cross_origin()
def askQuestion():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    user_knowledgestate = KnowledgeState.query.filter_by(user_id=user.id).first()
    knowledge = user_knowledgestate.knowledge
    user_chat = ChatLog.query.filter_by(user_id=user.id).first()
    ideasData = []
    ideas = Idea.query.filter_by(user_id=user.id).all()
    ideasData = [{"id": idea.id, "title": idea.title, "problem": idea.target_problem, "idea": idea.idea} for idea in ideas]

    instruction = ""

    if user_knowledgestate.counter['q_count'] >= 3:
        instruction = "Ask for the reviewer's own opinion or advice on the previous reviewer's question."
    elif user_knowledgestate.counter['q_count'] <= -3:
        instruction = "Ask what I need to think about to respond to the feedback."
    elif user_knowledgestate.counter['d_count'] >= 3:
        instruction = "Ask questions to synthesize what we've discussed so far."
    elif user_knowledgestate.counter['d_count'] <= -3:
        instruction = "Ask questions to expand on what we've discussed so far."
    elif user_knowledgestate.counter['r_count'] >= 3:
        instruction = "Ask questions that are relevant to what we're discussing."
    elif user_knowledgestate.counter['h_count'] >= 3:
        instruction = "Ask questions that elicit feedback that lead to higher-level thinking."
    elif user_knowledgestate.counter['s_count'] >= 3:
        instruction = "Ask questions that elicit specific feedback."
    elif user_knowledgestate.counter['j_count'] >= 3:
        instruction = "Ask questions that elicit justification."
    elif user_knowledgestate.counter['a_count'] >= 3:
        instruction = "Ask questions that elicit actionable feedback."
    elif user_knowledgestate.counter['u_count'] >= 3:
        instruction = "Ask questions to get feedback you hadn't considered."

    user_knowledgestate.counter = {'q_count': 0, 'd_count': 0, 'u_count': 0, 'r_count': 0, 'h_count': 0, 's_count': 0, 'j_count': 0, 'a_count': 0}
    
    question_prompt = [{"role": "system", "content":"This is your design ideas: " + json.dumps(ideasData) + "\nYour Design Knowledge: " + knowledge + "\nYou are a student who is trying to learn design. You're coming up with ideas for a design project. Your persona is \n* a Design Department 1st year student. \n* Korean. (say in Korean) \n* Speak colloquially only. Use honorifics.\n\nAsk questions to get good feedback from your feedback providers.The feedback meets the following conditions.\n* The question is aimed at finding knowledge that is not in my design knowledge that I need to know to answer the LAST feedback provider's question.\n*" + instruction + "\n* Keep your questions concise, in one sentence.\nThe format of your question is JSON as follows. {\"question\": {your question}} \nThis is previous conversations between you(the student) and the feedback provider: " + json.dumps(user_chat.log)}, 
                    {"role": "user", "content":"I am an industrial design expert. As a mento, I'll give feedback on your design project."}]

    completion1 = openai.chat.completions.create(
        model="gpt-4o",
        # model="gpt-3.5-turbo",
        messages=question_prompt,
        response_format={"type": "json_object"}
    )
    try:
        result = json.loads(completion1.choices[0].message.content)
    except ZeroDivisionError as e:
        # This will run only if there is no error
        return {"response": "죄송합니다...질문이 있었는데 까먹었습니다..."}

    print(result)
    user_chat.log.append({"speaker": "student", "content": result["question"]})
    flag_modified(user_chat, 'log')
    flag_modified(user_knowledgestate, 'counter')

    db.session.commit()

    return {"response": result["question"]}

@main.route("/nextRound")
@jwt_required()
@cross_origin()
def nextRound():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    user.currentRound += 1

    flag_modified(user, 'currentRound')
    db.session.commit()

    return {"msg":"Next Round!"}

app = create_app()
if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True)