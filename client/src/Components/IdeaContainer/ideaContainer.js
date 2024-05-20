import React, { useState, useRef } from 'react';
import axios from 'axios';
import './ideaContainer.css'

export const IdeaContainer = (props) => {

    const[ideas, setIdeas] = useState(props.ideasData);
    const[currentIdea, setCurrentIdea] = useState(0);

    const ChangeIdea = (i) => {
        if(currentIdea != i) {
            setCurrentIdea(i);
        }
    }
    
    return(
        <>
            <div className='ideaContainerUI'>
                <div className='navbar'>
                    {ideas.map((idea, index)=>
                        <button className={currentIdea == index ? 'current ideaTag' : 'ideaTag'} key={index} onClick={() => ChangeIdea(index)}>
                            Idea {index + 1}
                        </button>
                    )}
                </div>
                <div className='ideaContainer'>
                    {ideas.map((idea, index) => (index === currentIdea) ?
                        <div className='ideaBox' key={index}>
                            <div className='ideatitle'>Title: {idea.title}</div>
                            <div className='subtitle'>Target Problem</div>
                            <div className='problem'>{idea.problem}</div>
                            <div className='subtitle'>Idea</div>
                            <div className='idea'>{idea.idea}</div>
                        </div>
                        :
                        null
                    )}
                </div>
            </div>
        </>
    )
}