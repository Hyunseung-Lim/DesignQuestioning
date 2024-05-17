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
                        <button className='ideaTag' key={index} onClick={() => ChangeIdea(index)}>
                            idea {index + 1}
                        </button>
                    )}
                </div>
                <div className='ideaContainer'>
                    {ideas.map((idea, index) => (index === currentIdea) ?
                        <div className='ideaBox' key={index}>
                            <div className='ideatitle'>Title: {idea.title}</div>
                            <div className='problem'>Problem: {idea.problem}</div>
                            <div className='idea'>Idea: {idea.idea}</div>
                        </div>
                        :
                        null
                    )}
                </div>
            </div>
        </>
    )
}