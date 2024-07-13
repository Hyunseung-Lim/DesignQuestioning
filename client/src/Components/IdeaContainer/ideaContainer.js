import React, { useState, useRef } from 'react';
import axios from 'axios';
import './ideaContainer.css'

export const IdeaContainer = (props) => {

    const[ideas, setIdeas] = useState(props.ideasData);
    const[currentDescription, setCurrentDescription] = useState(0);

    const ChangeDescription = (i) => {
        if(currentDescription !== i) {
            setCurrentDescription(i);
        }
    }
    
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
                            <div>인구위기(저출산, 고령화) 극복을 위한 ‘기술의 활용’ 아이디어</div> 
                            :
                            <div>1. 뿡뿡<br/>2. 뿡뿡</div>
                    }
                </div>
                <div className='ideaContainer'>
                    {ideas.map((idea, index) =>
                        <div className='ideaBox' key={index}>
                            <div className='ideatitle'>IDEA {index+1}: {idea.title}</div>
                            <div className='subtitle'>Target Problem</div>
                            <div className='problem'>{idea.problem}</div>
                            <div className='subtitle'>Idea</div>
                            <div className='idea'>{idea.idea}</div>
                        </div>
                    )}
                </div>
            </div>
        </>
    )
}