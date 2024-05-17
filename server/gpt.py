# -*- coding: utf-8 -*-
import openai
import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

def feedbackEvaluation(user, feedback):
    prompt = [{
            "role": "system",
            "content": ""
        }]
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=prompt,
        stop=['User: '],
        max_tokens=3000,
        temperature=1.3,
        presence_penalty=0.5,
        frequency_penalty=0.5,
    )



def summerize(answer):
    answer_text = answer["lucy_answer"]
    prompt = [{"role": "system", "content": "Please summarize following answer below in a maximum of 2 sentences. \n Answer: " + str(answer_text)}]
    completion56 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        stop=['User: '],
        max_tokens=2048,
        temperature=1.0,
        presence_penalty=0.5,
        frequency_penalty=0.5,
    )
    summerized = completion56["choices"][0]["message"]['content']
    result = {"lucy_answer": summerized}
    print("summerization received from GPT")
    return result


def get_paper_titles(author_id):
    print("ds")
    base_url = "https://api.semanticscholar.org/v1/author/"
    url = base_url + author_id
    response = requests.get(url)
    data = json.loads(response.text)

    current_year = datetime.now().year

    # Filter papers from the last 5 years and ensure they have a year
    recent_papers = [paper for paper in data['papers'] if paper.get('year') is not None and (current_year - paper['year']) <= 5]

    # Sort the papers by year
    sorted_papers = sorted(recent_papers, key=lambda paper: paper['year'])

    # Extract the titles and format them
    titles = [f"{paper['title']} ({paper['year']})" for paper in sorted_papers]
    print(titles)
    return titles


def getAuthorInformation(publication):
    if publication:
        prompt = [{"role": "system", "content": "The following list is single researchers' publication list. Please introduce the researcher's research agenda and domain. Rather than focusing on individual papers, address the overall trend and themes of the papers. Keep it brief and factual. Keep it concise with bullet style. Length should be with in 2 paragraph The publication list is sorted by newest to oldest. \n Publication list: " + str(publication)}]

        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=prompt,
            stop=['User: '],
            max_tokens=3000,
            temperature=1.3,
            presence_penalty=0.5,
            frequency_penalty=0.5,
        )
        introduction = completion["choices"][0]["message"]['content']
        print(introduction)
        return introduction
    else:
        return None
    
    

def getSeedQuestion_P(title, abstract, intro, publications):
    if title is None or abstract is None:
        print("No valid title or abstract found for given code.")
        return None
    if intro is None:
        prompt = [{"role": "system", "content": "I'm the podcast host and preparing an interview with the author to introduce the following paper. I need to create 5 questions to present the paper that elicits the author's perspective and view on the paper. Please Generate questions related to the paper in light of the author's publication list, topic, and agenda. IMPORTANT: Please make the Question concise. Put questions in an array format without numbering. \n Author information: " + intro + "Publication list: " + str(publications) + "\n Paper title: " + title + "\nAbstract: " + abstract}]

    else:
        prompt = [{"role": "system", "content": "I'm the podcast host and preparing an interview with the author to introduce the following paper. I need to create 5 questions to present the paper that elicits the author's perspective and view on the paper. Please Generate questions related to the paper in light of the author's publication list, topic, and agenda. IMPORTANT: Please make the Question concise. Put questions in an array format without numbering. \n Author information: " + intro + "Publication list: " + str(publications) + "\n Paper title: " + title + "\nAbstract: " + abstract}]

    completion98 = openai.ChatCompletion.create(
        model="gpt-4",
        messages=prompt,
        stop=['User: '],
        max_tokens=4000,
        temperature=1.3,
        presence_penalty=0.5,
        frequency_penalty=0.5,
    )
    question = completion98["choices"][0]["message"]['content']
    print(question)
    return question




def upload(title, question_set, user):
    doc_ref = db.collection(u'pilot_0809').document(title)
    timestamp = time.time()

    string = "question_set_created at: " + str(timestamp)   
    doc_ref.set({
        u'participant' : user,
        u'LatestQestionSet': question_set,
        string: question_set
    }, merge=True)

def upload_log(title, user, log, correspondingData):
    doc_ref = db.collection(u'pilot_0809').document(u'log_data')
    timestamp = time.time()
    string = user + str(timestamp)
    
    data_to_set = {
        string: {
            u'title' : title,
            u'user' : user,
            u'log' : log,
            u'correspondingData' : correspondingData,
            u'timestamp' : str(timestamp)
        }
    }
    
    doc_ref.set(data_to_set, merge=True)

    
def download(title):
    doc_ref = db.collection(u'pilot_0809').document(title)
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
        data = doc.to_dict()
        qData = data['LatestQestionSet']
        return qData
    else:
        print(u'No such document!')


def fetch_arxiv_paper(code):
    url = "https://arxiv.org/abs/" + str(code)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('meta', attrs={'property': 'og:title'})
        title_content = title['content'] if title else "No title found"

        abstract = soup.find('meta', attrs={'property': 'og:description'})
        abstract_content = abstract['content'] if abstract else "No abstract found"

        return title_content, abstract_content
    else:
        print(f"Failed. HTTP response code: {response.status_code}")
        return None, None

def fetch_arxiv_paper2(code):
    url = "https://arxiv.org/abs/" + str(code)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('meta', attrs={'property': 'og:title'})
        title_content = title['content'] if title else "No title found"

        abstract = soup.find('meta', attrs={'property': 'og:description'})
        abstract_content = abstract['content'] if abstract else "No abstract found"

        authors = soup.find_all('meta', attrs={'name': 'citation_author'})
        authors_content = [author['content'] for author in authors] if authors else "No authors found"

        return title_content, abstract_content, authors_content
    else:
        print(f"Failed. HTTP response code: {response.status_code}")
        return None, None, None


def getSeedQuestion(code, viewer):
    title, abstract = fetch_arxiv_paper(code)
    if title and abstract:

        prompt = [{"role": "system", "content": "I'm the host of a podcast and I'm preparing an interview with the author to introduce the following paper. I need to create key 5 questions to introduce the paper. The questions range from high-level questions like motivation, background, and future work or direction to low-level, detailed questions like experimental details and results. IMPORTANT: Please make Question consise and short. Put questions in an array format without numbering. \nInstruction: " + viewer + "\n Paper title: " + title + "\nAbstract: " + abstract}]

        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=prompt,
            stop=['User: '],
            max_tokens=4000,
            temperature=1.3,
            presence_penalty=0.5,
            frequency_penalty=0.5,
        )
        return completion["choices"][0]["message"]['content']
    else:
        return None


def getSeedQuestion_re(link, added, viewer):
    title, abstract = fetch_arxiv_paper(link)
    if title and abstract:
        prompt = [{"role": "system", "content": "I'm the host of a podcast and I'm preparing an interview with the author to introduce the following paper. I want to edit exisiting 5 key questions based on following instruction. "+" \nExisting questions: "+ str(added) + "\nInstruction:" + viewer +"IMPORTANT: Please make Question consise and short. Put only edited questions in an array format without numbering. \n Paper title: " + title + "\nAbstract: " + abstract}]

        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=prompt,
            stop=['User: '],
            max_tokens=4000,
            temperature=1.3,
            presence_penalty=0.5,
            frequency_penalty=0.5,
        )
        return completion["choices"][0]["message"]['content']
    else:
        return None

def getFUQuestion(title, abstract, question, answer):
    new_message3 = [{"role": "system", "content": "I'm the host of a podcast and I'm preparing an interview with the author to introduce the following paper. The questions range from high-level questions like motivation and background to low-level, detailed questions like experimental details and results. Paper title: " + title + "\nAbstract: " + abstract}]
    new_message3.append({"role": "user",
                        "content": "I want to develop following question and answer" + "\nQuestion: " + question + "\nAnswer: " + answer + "\nPlease create a 3 follow-up questions. IMPORTANT: Please make Question consise and short. Put questions in an array format without numbering."})
    completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=new_message3,
            stop=['User: '],
            max_tokens=4000,
            temperature=1.3,
            presence_penalty=0.5,
            frequency_penalty=0.5,
        )
    return completion["choices"][0]["message"]['content']




@app.get("/getMeta/{link}")
async def get_meta(link: str) -> dict:
    response_text = fetch_arxiv_paper2(link)
    if response_text is not None:
        current = {"meta": response_text}
        return current
    else:
        raise HTTPException(status_code=404, detail="paper not found")
        
        
@app.post("/get_lucy_answer")
async def calc(request: Request):
    body = await request.json()
    title = body['title']
    question = body['question']
    answer = getLucyA(title, question)
    if len(answer['lucy_answer']) > 500:
        result = summerize(answer)
        return result
    answer["lucy_answer"] = json.loads(answer["lucy_answer"])[0]
    return answer


@app.post("/getFUQuestion")
async def calc(request: Request):
    body = await request.json()
    title = body['title']
    abstract = body['abstract']
    question = body['question']
    answer = body['answer']
    FUquestions = getFUQuestion(title, abstract, question, answer)
    return FUquestions

@app.post("/getQestionsetData")
async def calc(request: Request):
    body = await request.json()
    title = body['title']
    answer = download(title)
    return answer

@app.post("/uploadQuestionSet")
async def calc(request: Request):
    body = await request.json()
    title = body['title']
    question_set = body['question_set']
    user = body['user']
    upload(title, question_set, user)

    
@app.post("/getQuestion/")
async def calc(request: Request):
    body = await request.json()
    link = body['url']
    
    # added = body['added']
    viewer = body['viewer']
    
    response_text = getSeedQuestion(link, viewer)
    if response_text is not None:
        current = {"questions": response_text}
        current["questions"] = json.loads(current["questions"])
        return current        
    else:
        raise HTTPException(status_code=404, detail="paper not found")

    
@app.post("/getPersonalizedQ/")
async def calc(request: Request):
    body = await request.json()
    title = body['title']
    abstract = body['abstract']
    authorInfo = body['authorInfo']
    intro = authorInfo['intro']
    pList = authorInfo['publicationList']
    response_text = getSeedQuestion_P(title, abstract, str(intro), str(pList))
    if response_text is not None:
        current = {"questions": response_text}
        current["questions"] = json.loads(current["questions"])
        return current        
    else:
        raise HTTPException(status_code=404, detail="paper not found")

    return current

@app.post("/saveAuthorInfo")
async def calc(request: Request):
    body = await request.json()
    authorID = body['authorID']
    pList = get_paper_titles(authorID)
    intro = getAuthorInformation(pList)
    return {"publicationList":pList, "intro":intro}


@app.post("/uploadUsageLog")
async def calc(request: Request):
    body = await request.json()
    title = body['title']
    user = body['user']
    log = body['log']
    correspondingData = body['correspondingData']
    upload_log(title, user, log, correspondingData)
    
