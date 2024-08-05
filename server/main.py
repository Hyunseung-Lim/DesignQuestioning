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
import random


load_dotenv()  # This loads the environment variables from .env

# Now you can access the environment variable
My_OpenAI_key = os.getenv('My_OpenAI_key')
openai.api_key = My_OpenAI_key

LLQ = ["low-level", "verification", "definition", "example", "feature specification", "concept completion", "quantification", "disjunctive", "comparison", "judgmental"]
DRQ = ["deep reasoning", "interpretation", "goal orientation", "causal antecedent", "causal consequent", "expectational", "instrumental/procedural", "instrumental", "procedural", "enablement(dr)"]
GDQ = ["generate design", "proposal/negotiation", "proposal", "negotiation", "scenario creation", "ideation", "method", "enablement(gd)"]

ideaOrder = [[0,2,1,3],[0,3,1,2],[1,2,0,3],[1,3,0,2],[2,0,3,1],[2,1,3,0],[3,0,2,1],[3,1,2,0]]

Ideas = [
    {'topic': "인구위기(저출산, 고령화) 극복을 위한 '기술의 활용' 아이디어", 'design_goals': ['1.', '2.', '3.'], 'title': "유아친화 지역 사회 공간", 'target_problem': "아이를 키우는 환경의 부족", 'idea': "지역 사회 내에서 안전하고 창의적인 유아친화 공간을 만들어 부모들이 아이들을 더욱 편리하고 즐겁게 키울 수 있도록 지원합니다. 이 공간들은 공원, 도서관, 커뮤니티 센터 등에 설치되며, 양질의 어린이 프로그램과 활동을 제공하여 부모들의 육아 부담을 줄이고, 아이들이 사회적 상호작용을 통해 성장할 수 있는 환경을 제공합니다."},
    {'topic': "유아 교육 장난감의 혁신을 통한 언어 능력 향상", 'design_goals': ['1. ', '2.', '3.'], 'title': "LingoKids: AI 기반 인터랙티브 언어 학습 블록", 'target_problem': "현재 유아 교육 장난감 시장에서 언어 학습을 위한 효과적인 도구가 부족합니다. 대부분의 장난감은 단순한 단어 반복에 집중되어 있어, 유아의 발음 정확성, 문장 구성 능력 등 실제 언어 사용에 필요한 능력을 충분히 개발하지 못하고 있습니다. 이는 부모가 아이의 언어 학습 진행 상황을 정확하게 파악하고 적절하게 지원하기 어렵게 만들며, 유아의 언어 발달에 필수적인 지속적인 피드백과 개인화된 학습 지원의 부재를 초래합니다.", 'idea': "LingoKids는 AI 기술을 통합하여 유아의 언어 학습을 지원하는 인터랙티브 학습 블록입니다. 이 시스템은 음성 인식 기술을 활용해 아이들의 발음과 언어 사용을 정확히 평가하고, AI가 제공하는 즉각적인 시각적 및 청각적 피드백을 통해 언어 학습을 강화합니다. 각 블록은 아이들이 다양한 언어 활동을 수행하도록 설계되어 있으며, 아이들이 단어를 말하거나 문장을 구성할 때마다 AI가 그 성능을 분석하여 아이의 언어 능력에 적합한 맞춤형 연습과 향상 방안을 제공합니다. 부모는 전용 모바일 앱을 통해 아이의 학습 진행 상황을 실시간으로 모니터링하고, AI로부터 제공받는 개인화된 조언을 바탕으로 집에서도 아이의 언어 학습을 적극적으로 지원할 수 있습니다. LingoKids는 유아의 언어 발달을 자극하고, 언어 학습의 기초를 견고히 함으로써 언어 능력의 전반적인 향상을 도모합니다."},
    {'topic': "헬스케어 혁신을 통한 개선된 수면 및 호흡 관리", 'design_goals': ['1. ', '2.', '3.'], 'title': "SleepWell: AI 기반 개인 맞춤형 수면 및 호흡 관리 시스템", 'target_problem': "수면의 질은 건강에 직접적인 영향을 미치지만, 많은 사람들이 불규칙한 수면 패턴, 수면 중 호흡 장애 등으로 인해 효과적인 수면을 취하지 못하고 있습니다. 현재 시장에는 이러한 문제를 해결할 수 있는 통합적이고 개인화된 솔루션의 부족으로, 수면 장애를 가진 개인들이 적절한 진단과 관리를 받기 어렵습니다.", 'idea': "SleepWell은 사용자의 수면 패턴과 호흡 상태를 모니터링하고, 인공지능을 활용하여 개인 맞춤형 수면 개선 계획을 제공하는 통합 헬스케어 솔루션입니다. 이 시스템은 수면 중에 착용하는 센서 기반의 웨어러블 디바이스와 연동되어, 실시간으로 수면의 질과 호흡 패턴을 분석합니다. AI 알고리즘은 수집된 데이터를 기반으로 사용자의 수면 습관을 평가하고, 수면의 질을 최적화하기 위한 맞춤형 조언과 개선 방안을 제시합니다. 이 디바이스는 또한 수면 중 발생할 수 있는 호흡 중단과 같은 이상 징후를 감지하고, 필요한 경우 사용자나 의료 전문가에게 경고를 보냅니다. 사용자는 관련 앱을 통해 자신의 수면 패턴과 호흡 질을 추적하고, 개선된 수면 습관을 위한 목표 설정과 진행 상황을 확인할 수 있습니다. 이를 통해 SleepWell은 수면의 질을 향상시키고, 수면 관련 건강 문제를 예방하는 데 기여합니다."},
    {'topic': "인구위기(저출산, 고령화) 극복을 위한 '기술의 활용' 아이디어", 'design_goals': ['1. ', '2.', '3.'], 'title': "유아친화 지역 사회 공간", 'target_problem': "아이를 키우는 환경의 부족", 'idea': "지역 사회 내에서 안전하고 창의적인 유아친화 공간을 만들어 부모들이 아이들을 더욱 편리하고 즐겁게 키울 수 있도록 지원합니다. 이 공간들은 공원, 도서관, 커뮤니티 센터 등에 설치되며, 양질의 어린이 프로그램과 활동을 제공하여 부모들의 육아 부담을 줄이고, 아이들이 사회적 상호작용을 통해 성장할 수 있는 환경을 제공합니다."},
    {'topic': "인구위기(저출산, 고령화) 극복을 위한 '기술의 활용' 아이디어", 'design_goals': ['1. ', '2.', '3.'], 'title': "유아친화 지역 사회 공간", 'target_problem': "아이를 키우는 환경의 부족", 'idea': "지역 사회 내에서 안전하고 창의적인 유아친화 공간을 만들어 부모들이 아이들을 더욱 편리하고 즐겁게 키울 수 있도록 지원합니다. 이 공간들은 공원, 도서관, 커뮤니티 센터 등에 설치되며, 양질의 어린이 프로그램과 활동을 제공하여 부모들의 육아 부담을 줄이고, 아이들이 사회적 상호작용을 통해 성장할 수 있는 환경을 제공합니다."},
    {'topic': "인구위기(저출산, 고령화) 극복을 위한 '기술의 활용' 아이디어", 'design_goals': ['1. ', '2.', '3.'], 'title': "유아친화 지역 사회 공간", 'target_problem': "아이를 키우는 환경의 부족", 'idea': "지역 사회 내에서 안전하고 창의적인 유아친화 공간을 만들어 부모들이 아이들을 더욱 편리하고 즐겁게 키울 수 있도록 지원합니다. 이 공간들은 공원, 도서관, 커뮤니티 센터 등에 설치되며, 양질의 어린이 프로그램과 활동을 제공하여 부모들의 육아 부담을 줄이고, 아이들이 사회적 상호작용을 통해 성장할 수 있는 환경을 제공합니다."},
    {'topic': "인구위기(저출산, 고령화) 극복을 위한 '기술의 활용' 아이디어", 'design_goals': ['1. ', '2.', '3.'], 'title': "유아친화 지역 사회 공간", 'target_problem': "아이를 키우는 환경의 부족", 'idea': "지역 사회 내에서 안전하고 창의적인 유아친화 공간을 만들어 부모들이 아이들을 더욱 편리하고 즐겁게 키울 수 있도록 지원합니다. 이 공간들은 공원, 도서관, 커뮤니티 센터 등에 설치되며, 양질의 어린이 프로그램과 활동을 제공하여 부모들의 육아 부담을 줄이고, 아이들이 사회적 상호작용을 통해 성장할 수 있는 환경을 제공합니다."},
    {'topic': "인구위기(저출산, 고령화) 극복을 위한 '기술의 활용' 아이디어", 'design_goals': ['1. ', '2.', '3.'], 'title': "유아친화 지역 사회 공간", 'target_problem': "아이를 키우는 환경의 부족", 'idea': "지역 사회 내에서 안전하고 창의적인 유아친화 공간을 만들어 부모들이 아이들을 더욱 편리하고 즐겁게 키울 수 있도록 지원합니다. 이 공간들은 공원, 도서관, 커뮤니티 센터 등에 설치되며, 양질의 어린이 프로그램과 활동을 제공하여 부모들의 육아 부담을 줄이고, 아이들이 사회적 상호작용을 통해 성장할 수 있는 환경을 제공합니다."},
]

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
    
    idea = Idea.query.filter_by(user_id=user.id, round=user.currentRound).first()
    ideaData = {"id": idea.id, "topic": idea.topic, "design_goals": idea.design_goals, "title": idea.title, "problem": idea.target_problem, "idea": idea.idea}
    # ideasData = []
    # ideas = Idea.query.filter_by(user_id=user.id, round=user.currentRound).all()
    # ideasData = [{"id": idea.id, "title": idea.title, "problem": idea.target_problem, "idea": idea.idea} for idea in ideas]
    
    userChat = ChatLog.query.filter_by(user_id=user.id, round=user.currentRound).first()
    setting = InitialSetting.query.filter_by(user_id=user.id, round=user.currentRound).first()
    
    if setting.mode == 1 :
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

        return {"ideaData": ideaData, "chatData": userChat.log, "name": name, "mode": setting.mode, "character": setting.character, "goal1": setting.goal1, "goal2": setting.goal2, "goal3": setting.goal3, "time": setting.time, "student_knowledge_level": len(user_knowledgestate.knowledge), "qns": user_knowledgestate.qns, "cnd": user_knowledgestate.cnd, "uniqueness": feedback_uniqueness, "relevance": feedback_relevance, "high_level": feedback_high_level, "specificity": feedback_specificity, "justification": feedback_justification, "active": feedback_active, 'face': user_knowledgestate.face}
    
    return  {"ideaData": ideaData, "chatData": userChat.log, "name": name, "mode": setting.mode, "character": "", "goal1": "", "goal2": "", "goal3": "", "time": setting.time, "student_knowledge_level": "", "qns": "", "cnd": "", "uniqueness": "", "relevance": "", "high_level": "", "specificity": "", "justification": "", "active": "", 'face': ""}

@main.route("/mode", methods=["POST"])
@jwt_required()
@cross_origin()
def mode():
    params = request.get_json()
    user_mode = params['mode']
    user = User.query.filter_by(email=get_jwt_identity()).first()

    new_settings = [
        InitialSetting(user_id=user.id, mode= user_mode, round=1, character = 0, goal1="", goal2="", goal3="", time = 20),
        InitialSetting(user_id=user.id, mode= user_mode, round=2, character = 0, goal1="", goal2="", goal3="", time = 20),
        InitialSetting(user_id=user.id, mode= 3 - user_mode, round=3, character = 0, goal1="", goal2="", goal3="", time = 20),
        InitialSetting(user_id=user.id, mode= 3 - user_mode, round=4, character = 0, goal1="", goal2="", goal3="", time = 20)
    ]
    
    new_ideas = [
        Idea(user_id=user.id, round=1, design_goals = Ideas[ideaOrder[user.id % 8][0] * 2 + random.choice([0, 1])]['design_goals'], topic=Ideas[ideaOrder[user.id % 8][0] * 2 + random.choice([0, 1])]['topic'], title=Ideas[ideaOrder[user.id % 8][0] * 2 + random.choice([0, 1])]['title'], target_problem=Ideas[ideaOrder[user.id % 8][0] * 2 + random.choice([0, 1])]['target_problem'], idea=Ideas[ideaOrder[user.id % 8][0] * 2 + random.choice([0, 1])]['idea']),
        Idea(user_id=user.id, round=2, design_goals = Ideas[ideaOrder[user.id % 8][1] * 2 + random.choice([0, 1])]['design_goals'], topic=Ideas[ideaOrder[user.id % 8][1] * 2 + random.choice([0, 1])]['topic'], title=Ideas[ideaOrder[user.id % 8][1] * 2 + random.choice([0, 1])]['title'], target_problem=Ideas[ideaOrder[user.id % 8][1] * 2 + random.choice([0, 1])]['target_problem'], idea=Ideas[ideaOrder[user.id % 8][1] * 2 + random.choice([0, 1])]['idea']),
        Idea(user_id=user.id, round=3, design_goals = Ideas[ideaOrder[user.id % 8][2] * 2 + random.choice([0, 1])]['design_goals'], topic=Ideas[ideaOrder[user.id % 8][2] * 2 + random.choice([0, 1])]['topic'], title=Ideas[ideaOrder[user.id % 8][2] * 2 + random.choice([0, 1])]['title'], target_problem=Ideas[ideaOrder[user.id % 8][2] * 2 + random.choice([0, 1])]['target_problem'], idea=Ideas[ideaOrder[user.id % 8][2] * 2 + random.choice([0, 1])]['idea']),
        Idea(user_id=user.id, round=4, design_goals = Ideas[ideaOrder[user.id % 8][3] * 2 + random.choice([0, 1])]['design_goals'], topic=Ideas[ideaOrder[user.id % 8][3] * 2 + random.choice([0, 1])]['topic'], title=Ideas[ideaOrder[user.id % 8][3] * 2 + random.choice([0, 1])]['title'], target_problem=Ideas[ideaOrder[user.id % 8][3] * 2 + random.choice([0, 1])]['target_problem'], idea=Ideas[ideaOrder[user.id % 8][3] * 2 + random.choice([0, 1])]['idea'])
    ]
    
    if user_mode == 1:
        new_KnowledgeStates = [
            KnowledgeState(user_id = user.id, round=1, face=33, q_num=0, s_num=0, qns=0, cnd=0, eval={'uniqueness': 0, 'relevance': 0, 'high-level': 0, 'specificity': 0, 'justification': 0, 'active': 0}, knowledge = "", counter={'q_count': 0, 'd_count': 0, 'u_count': 0, 'r_count': 0, 'h_count': 0, 's_count': 0, 'j_count': 0, 'a_count': 0}),
            KnowledgeState(user_id = user.id, round=2, face=33, q_num=0, s_num=0, qns=0, cnd=0, eval={'uniqueness': 0, 'relevance': 0, 'high-level': 0, 'specificity': 0, 'justification': 0, 'active': 0}, knowledge = "", counter={'q_count': 0, 'd_count': 0, 'u_count': 0, 'r_count': 0, 'h_count': 0, 's_count': 0, 'j_count': 0, 'a_count': 0}),
        ]
        new_ChatLogs = [
            ChatLog(user_id = user.id, round=1, log = [{"speaker":"student", "content": "안녕하세요! 저는 동건이라고 합니다. 제 아이디어에 대한 피드백을 주시면 감사하겠습니다."}]),
            ChatLog(user_id = user.id, round=2, log = [{"speaker":"student", "content": "안녕하세요! 저는 동건이라고 합니다. 제 아이디어에 대한 피드백을 주시면 감사하겠습니다."}]),
            ChatLog(user_id = user.id, round=3, log = [{"speaker":"student", "content": "안녕하세요! 제 아이디어에 대한 피드백을 주시면 감사하겠습니다."}]),
            ChatLog(user_id = user.id, round=4, log = [{"speaker":"student", "content": "안녕하세요! 제 아이디어에 대한 피드백을 주시면 감사하겠습니다."}])
        ]
    
    else:
        new_KnowledgeStates = [
            KnowledgeState(user_id = user.id, round=3, face=33, q_num=0, s_num=0, qns=0, cnd=0, eval={'uniqueness': 0, 'relevance': 0, 'high-level': 0, 'specificity': 0, 'justification': 0, 'active': 0}, knowledge = "", counter={'q_count': 0, 'd_count': 0, 'u_count': 0, 'r_count': 0, 'h_count': 0, 's_count': 0, 'j_count': 0, 'a_count': 0}),
            KnowledgeState(user_id = user.id, round=4, face=33, q_num=0, s_num=0, qns=0, cnd=0, eval={'uniqueness': 0, 'relevance': 0, 'high-level': 0, 'specificity': 0, 'justification': 0, 'active': 0}, knowledge = "", counter={'q_count': 0, 'd_count': 0, 'u_count': 0, 'r_count': 0, 'h_count': 0, 's_count': 0, 'j_count': 0, 'a_count': 0}),
        ]
        new_ChatLogs = [
            ChatLog(user_id = user.id, round=1, log = [{"speaker":"student", "content": "안녕하세요! 제 아이디어에 대한 피드백을 주시면 감사하겠습니다."}]),
            ChatLog(user_id = user.id, round=2, log = [{"speaker":"student", "content": "안녕하세요! 제 아이디어에 대한 피드백을 주시면 감사하겠습니다."}]),
            ChatLog(user_id = user.id, round=3, log = [{"speaker":"student", "content": "안녕하세요! 저는 동건이라고 합니다. 제 아이디어에 대한 피드백을 주시면 감사하겠습니다."}]),
            ChatLog(user_id = user.id, round=4, log = [{"speaker":"student", "content": "안녕하세요! 저는 동건이라고 합니다. 제 아이디어에 대한 피드백을 주시면 감사하겠습니다."}])
        ]
    
    db.session.add_all(new_settings + new_ideas + new_KnowledgeStates + new_ChatLogs)
    db.session.flush()
    db.session.commit()
    
    return {"msg": "select mode"}

@main.route("/getSetting")
@jwt_required()
@cross_origin()
def getSetting():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    currentRound = user.currentRound
    if currentRound >= 5:
        return {"msg": "Done!"}
    setting = InitialSetting.query.filter_by(user_id=user.id, round=currentRound).first()
    
    return {"mode": setting.mode, "round": currentRound, "character": setting.character, "goal1": setting.goal1, "goal2": setting.goal2, "goal3": setting.goal3, "time": setting.time}


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
        
    if currentRound <=4:        
        setting4 = InitialSetting.query.filter_by(user_id=user.id, round=4).first()
        setting4.character = current_character
        setting4.goal1 = current_goal1
        setting4.goal2 = current_goal2
        setting4.goal3 = current_goal3
        setting4.time = current_time
        flag_all_modified(setting4)
    
    db.session.commit()
    return {"msg": "save the current setting"}

@main.route("/response", methods=["POST"])
@jwt_required()
@cross_origin()
def response():
    params = request.get_json()
    feedback = params['feedback']
    user = User.query.filter_by(email=get_jwt_identity()).first()
    
    idea = Idea.query.filter_by(user_id=user.id, round=user.currentRound).first()
    ideaData = {"topic": idea.topic, "design criteria": idea.design_goals, "title": idea.title, "problem": idea.target_problem, "idea": idea.idea}
    
    user_knowledgestate = KnowledgeState.query.filter_by(user_id=user.id, round=user.currentRound).first()
    # opportunity = user_knowledgestate.opportunity
    # consideration = user_knowledgestate.consideration
    knowledge = user_knowledgestate.knowledge
    user_chat = ChatLog.query.filter_by(user_id=user.id, round=user.currentRound).first()

    feedbackcate_prompt = [{"role": "system", "content":"Feedback Analysis Instructions for Instructor's Feedback of a Student's Design Idea.\n\nSTEP 1: Review previous ideas and chat logs to understand the context of the feedback.\n\nSTEP 2: Decompose the feedback into individual sentences.\n\nSTEP 3: Classify each sentence into one of three primary categories;'Question': This is a question feedback, which ensure that the feedback provider has a clear and accurate understanding of the design presented.;'Statement': This is a statement feedback, which provides relevant information or is directly related to a design idea to evaluate or suggest improvements.;'No feedback': This sentence is completely irrelevant to the feedback.\n\nSTEP 4: Subcategorize each sentence based on its nature (There are 21 types of 'Question', three types of 'Statement' and no sub category for 'No feedback.'); 'Question':\n\"Low-Level\": Seeks factual details about the design.\n- Verification: Is X true?\n- Definition: What does X mean?\n- Example: What is an example of X?\n- Feature Specification: What (qualitative) attributes does X have?\n- Concept Completion: Who? What? When? Where?\n- Quantification: How much? How many?\n- Disjunctive: Is X or Y the case?\n- Comparison: How does X compare to Y?\n- Judgmental: What is your opinion on X?\n\"Deep Reasoning\": Explores deeper implications or reasons behind the design.\n- Interpretation: How is a particular event or pattern of information interpreted or summarized?\n- Goal Orientation: What are the motives behind an agent’s action?\n- Causal Antecedent: What caused X to occur?\n- Causal Consequent: What were the consequences of X occurring?\n- Expectational: Why is X not true?\n- Instrumental/Procedural: How does an agent accomplish a goal?\n- Enablement(DR): What object or resource enables an agent to perform an action?\n\"Generate Design\": Encourages innovative thinking about design challenges.\n- Proposal/Negotiation: Could a new concept be suggested/negotiated?\n- Scenario Creation: What would happen if X occurred?\n- Ideation: Generation of ideas without a deliberate end goal\n- Method: How could an agent accomplish a goal?\n- Enablement(GD): What object or resource could enable an agent to perform an action?\n'Statement':\n\"Information\": Share related information or examples.\n\"Evaluation\": Assess the student’s design idea. Stating general facts rather than evaluating a student's ideas doesn't belong.\n\"Recommendation\": Provide actionable suggestions for improvement.\n\nSTEP 5: Summarize the extracted knowledge from each category. Knowledge includes only key approaches and keywords and excludes complex context.\n'Question':\n\"Low-Level\": DO NOT ADD knowledge.\n\"Deep Reasoning\": Suggest design considerations.\n\"Generate Design\": Suggest new design opportunities.\n'Statement':\n\"Information\": Details the provided information.\n\"Evaluation\": Describes the assessment of the design.\n\"Recommendation\": Outline ideas for enhancement.\n'No feedback': DO NOT ADD knowledge.\n\nSTEP 6: Check whether the knowledge is already known to the student or not.\n\nResponse Only in JSON array, which looks like, {\"sentences\":[{\"sentence\": \"\", \"categories\":\"\", \"type\":\"\", \"knowledge\":\"\", \"isNew\":\"\"}]}.\n\"sentence\": Individual unit of feedback.\n\"categories\": Category of feedback. ('Question' or 'Statement' or 'No feedback')\n\"type\": Subcategory of feedback (e.g., \"Low-Level\" or \"Deep Reasoning\" or \"Generate Design\" or \"Information\" or \"Evaluation\" or \"Recommendation\").\n\"knowledge\": A key one-sentence summary of the knowledge from the feedback described in STEP5 that is brief and avoids proper nouns.\n\"isNew\": If it's new knowledge, true; otherwise, false.\nStudent's Idea:" + json.dumps(ideaData, ensure_ascii=False) + "\nStudent's Knowledge:" + knowledge + "\nchat Log:" + json.dumps(user_chat.log, ensure_ascii=False) + "\nfeedback:" + feedback}]
    student_prompt = [{"role": "system", "content":"This is your design idea: " + json.dumps(ideaData, ensure_ascii=False) + "\nYou are a student who is trying to learn design. You're coming up with ideas for a design project. Your persona is \n* A Design Department 1st year student. \n* Korean. (say in Korean) \n* NEVER apologize, NEVER say you can help, and NEVER just say thanks.\n* NEVER write more than 3 sentences in a single response. Speak colloquially only. Use honorifics.\n\nAnswer feedback from the mentor ONLY based on your knowledge. If you can't answer based on Your Design Knowledge, say sorry, I don't know. BUT try to answer AS MUCH AS you can.\n\nThe format of your answer is JSON as follows. {\"answer\": {your answer}} \nThese are previous conversations between you(the student) and the mentor: " + json.dumps(user_chat.log, ensure_ascii=False) + "\nThis is the mentor's following chat(feedback): " + feedback}, 
                      {"role": "user", "content":"I am an industrial design expert. As a mentor, I'll give feedback on your design project."}]

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

    feedbackeval_prompt = [{"role": "system", "content":"Feedback Evaluation Instructions for Instructor's Feedback of a Student's Design Idea.\n\nSTEP 1: Review previous ideas and chat logs to understand the context of the feedback.\n\nSTEP 2: Evaluate the feedback on a scale of 1 to 57 based on the following criteria. There are three different criteria depending on whether the feedback category is a 'Question' or a 'Statement'.\n'Question':\n\"uniqueness\": The question is unique.\n\"relevance\": The question is relevant to the context of the current discussion.\n\"high-level\": The question is high-level.(If the question falls into the \"Low-Level\" category, it's between 1 and 2. Otherwise, it's between 3 and 5.)\n'Statement':\n\"specificity\": The feedback is specific.\n\"justification\": The feedback is justified.\n\"active\": The feedback is actionable\n'No feedback': DO NOT RATE.\nSTEP 3: Evaluate the sentiment of the feedback. Analyze the sentiment of the feedback and rate it as either positive(1), neutral(0), or negative(-1).\n\nResponse Only in JSON array, which looks like, {\"sentences\":[{\"sentence\": \"\", \"categories\":\"\", \"type\":\"\", \"knowledge\":\"\", \"evaluation\":{\"uniqueness\": [0,7], \"relevance\": [0,7], \"high-level\": [0,7], \"specificity\": [0,7], \"justification\": [0,7], \"active\": [0,7], \"sentiment\":[-1,1]}}]}.\n\"sentence\": Individual unit of feedback.\n\"categories\": Category of feedback. ('Question' or 'Statement' or 'No feedback')\n\"type\": Subcategory of feedback (e.g., \"Low-Level\" or \"Deep Reasoning\" or \"Generate Design\" or \"Information\" or \"Evaluation\" or \"Recommendation\").\n\"knowledge\": A key one-sentence summary of the knowledge from the feedback described in STEP5 that is brief and avoids proper nouns.\n\"evaluation\": JSON with the evaluation score based on the criteria. The criteria that should be evaluated in STEP 2 have a value between 1-7, with the rest evaluated as 0.\n\nStudent's Idea:" + json.dumps(ideaData, ensure_ascii=False) + "\nchat Log:" + json.dumps(user_chat.log, ensure_ascii=False) + "\nfeedback:" + str(result1)}]

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
    
                if sentence['type'].lower() in ['information', 'evaluation', 'recommendation']:
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

@main.route("/baselineresponse", methods=["POST"])
@jwt_required()
@cross_origin()
def baselineresponse():
    params = request.get_json()
    feedback = params['feedback']
    user = User.query.filter_by(email=get_jwt_identity()).first()
    
    idea = Idea.query.filter_by(user_id=user.id, round=user.currentRound).first()
    ideaData = {"topic": idea.topic, "design criteria": idea.design_goals, "title": idea.title, "problem": idea.target_problem, "idea": idea.idea}

    user_chat = ChatLog.query.filter_by(user_id=user.id, round=user.currentRound).first()

    prompt = [{"role": "system","content":"This is your design ideas: " + json.dumps(ideaData, ensure_ascii=False) + "\nAnswer feedback from the user.\nThe format of your answer is JSON as follows. {\"answer\": {your answer}} \nYour answer can only be text, not an array.(markdown is available.)\nThis is previous conversations: " + json.dumps(user_chat.log, ensure_ascii=False) + "\nThis is the following chat(feedback): " + feedback }]
            
    completion = openai.chat.completions.create(
        model="gpt-4o",
        # model="gpt-3.5-turbo",
        messages=prompt,
        response_format={"type": "json_object"}
    )
    try:
        result3 = json.loads(completion.choices[0].message.content)
    except ZeroDivisionError as e:
    # This will run only if there is no error
        return {"response": "죄송합니다...제가 잘 이해 못한 거 같아요. 다시 말씀해주실 수 있을까요?"}

    new_entries = [
        {"speaker": "instructor", "content": feedback},
        {"speaker": "student", "content": result3["answer"]}
    ]
    user_chat.log.extend(new_entries)
    flag_modified(user_chat, 'log')

    db.session.commit()
    return {"response": result3["answer"]}


@main.route("/askQuestion")
@jwt_required()
@cross_origin()
def askQuestion():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    user_knowledgestate = KnowledgeState.query.filter_by(user_id=user.id).first()
    knowledge = user_knowledgestate.knowledge
    user_chat = ChatLog.query.filter_by(user_id=user.id).first()
    idea = Idea.query.filter_by(user_id=user.id, round=user.currentRound).first()
    ideaData = {"topic": idea.topic, "design criteria": idea.design_goals, "title": idea.title, "problem": idea.target_problem, "idea": idea.idea}

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
    
    formatted_chat = ''.join([f'you: {x["content"]}\n' if x["speaker"] == "student" else f'mentor: {x["content"]}\n' for x in user_chat.log])
    formatted_knowledge = knowledge.replace(".", ".\n")
    question_prompt = [
        {
            "role": "system",
            "content": f"""
You are a student who is trying to learn design. You're coming up with ideas for a design project. Your persona is:
* a Design Department 1st year student.
* Korean. (say in Korean)
* Speak colloquially only. Use honorifics.

This is your current design idea:
* Topic: {ideaData['topic']}
* Title: {ideaData['title']}
* Problem: {ideaData['problem']}
* Idea: {ideaData['idea']}

These are previous conversations between you (the student) and the mentor about your design idea:
{formatted_chat}

This is your current design knowledge accumulated by the conversation with your mentor:
{formatted_knowledge}

Now, you need to ask questions to get more feedback from your mentor. {instruction} You should not ask for direct answers to your design idea, but you need to ask some questions that can elicit feedback on it.

Your question can be one of the following types:
* Brainstorm: Ask about tactics or strategies to think about more ideas.
* Critique: Directly ask for feedback on your design. Your question should not be asking for general feedback but rather focusing on a specific aspect of your design.
* Improve: Ask a question about how to improve your design. Your question should not be asking for a solution but rather a direction or actions that you need to do.
* Share: Ask your mentor about their experience or knowledge of the current topic.

Your question should help you find knowledge not in your current design knowledge, but you need to know how to answer the last mentor's question. Keep your questions concise, no more than one sentence.

The format of your question is JSON as follows:
{{"question": "your question"}}
        """
        },
        {"role": "user", "content": "I am an industrial design expert. As a mentor, I'll give feedback on your design project."},
    ]

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

@main.route("/updateIdea")
@jwt_required()
@cross_origin()
def updateIdea():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    user_chat = ChatLog.query.filter_by(user_id=user.id).first()
    idea = Idea.query.filter_by(user_id=user.id, round=user.currentRound).first()
    ideaData = {"topic": idea.topic, "design criteria": idea.design_goals, "title": idea.title, "problem": idea.target_problem, "idea": idea.idea}
    ideaUpdatePrompt = [{ "role": "system", "content":"PLEASE improve your design ideas by incorporating the following conversation as much as possible. All content must be written in Korean.\nThis is a design idea you have to improve;" + json.dumps(ideaData, ensure_ascii=False) + "\nThis is the conversation you have to refer to;" + json.dumps(user_chat.log, ensure_ascii=False) + "\nResponse Only in JSON array, which looks like, {'title': \"\", 'target_problem': \"\", 'idea': \"\"}"}]
    
    completion1 = openai.chat.completions.create(
        model="gpt-4-turbo",
        # model="gpt-3.5-turbo",
        messages=ideaUpdatePrompt,
        response_format={"type": "json_object"}
    )
    try:
        result = json.loads(completion1.choices[0].message.content)
    except ZeroDivisionError as e:
        # This will run only if there is no error
        return {"response": "error"}
    
    try:
        idea.title = result['title']
        idea.problem = result['target_problem']
        idea.idea = result['idea']

        flag_modified(idea, 'title')
        flag_modified(idea, 'target_problem')
        flag_modified(idea, 'idea')
        db.session.commit()

    except ZeroDivisionError as e:
        return {"response": "error"}
    
    ideaData = {"topic": idea.topic, "design criteria": idea.design_goals, "title": result['title'], "problem": result['target_problem'], "idea": result['idea']}

    return {"ideaData": ideaData}



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