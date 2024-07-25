import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './ideaContainer.css'

export const IdeaContainer = (props) => {

    const[idea, setIdea] = useState(props.ideaData);
    const[currentDescription, setCurrentDescription] = useState(0);

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
                            <div>{idea.topic}</div> 
                            :
                            <div>{idea.design_goals.map((goal, index) => <div key={index}>{goal}</div>)}</div>
                    }
                </div>
                <div className='ideaContainer'>
                    <div className='ideaBox'>
                        <div className='ideatitle'><div className='title'>IDEA: {idea.title}</div><button onClick={UpdateIDea}>Update Idea</button></div>
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