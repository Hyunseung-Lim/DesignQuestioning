import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './ideaContainer.css'

export const IdeaContainer = (props) => {

    const [idea, setIdea] = useState(props.ideaData);
    const [isUpdateIdea, setIsUpdateIdea] = useState(props.isUpdateIdea);
    const [currentDescription, setCurrentDescription] = useState(0);

    const ChangeDescription = (i) => {
        if(currentDescription !== i) {
            setCurrentDescription(i);
        }
    }

    const UpdateIDea = () => {
        props.updateIdea();
    }

    useEffect(()=> {
        setIdea(props.ideaData);
    }, [props.ideaData]);

    useEffect(()=> {
        setIsUpdateIdea(props.isUpdateIdea);
    }, [props.isUpdateIdea]);
    
    return(
        <>
            <div className='ideaContainerUI'>
                <div className='navbar'>
                    <button className={currentDescription === 1 ? 'current Tag' : 'Tag'} onClick={() => ChangeDescription(0)}>
                        Topic
                    </button>
                    <button className={currentDescription === 0 ? 'current right Tag' : 'right Tag'} onClick={() => ChangeDescription(1)}>
                        Design Goals
                    </button>
                </div>
                <div className='ideaDescription'>
                    {
                        currentDescription === 0 ? 
                            <div className='topic'>{idea.topic}</div> 
                            :
                            <div className='goalsConatiner'>
                                <div className='design_goal'><b>Inovation:</b> 아이디어가 얼마나 혁신적인 지</div> 
                                <div className='design_goal'><b>Elaboration:</b> 아이디어가 얼마나 정교한지</div> 
                                <div className='design_goal'><b>Usability:</b> 아이디어가 얼마나 사용하기 용이한지</div>
                                <div className='design_goal'><b>Value:</b> 아이디어가 얼마나 사용할 가치가 있는지</div>
                                <div className='design_goal'><b>Social Responsiblity:</b> 아이디어가 얼마나 사회적 책임을 이행하는지</div>
                            </div>
                    }
                </div>
                <div className='ideaContainer'>
                    <div className={isUpdateIdea ? 'ideaBox disable' : 'ideaBox'}>
                        <div className='ideatitle'><div className='title'>{idea.title}</div><button onClick={UpdateIDea} disabled={isUpdateIdea}>Update Idea</button></div>
                        <div className='subtitle'>Target Problem</div>
                        <div className='problem'>{idea.problem}</div>
                        <div className='subtitle'>Idea</div>
                        <div className='idea'>{idea.idea}</div>
                    </div>
                </div>
            </div>
        </>
    )
}