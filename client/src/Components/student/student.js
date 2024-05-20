import React, {useState, useEffect} from 'react';
import './student.css'

export const Student = (props) => {

    const [divergentLevel, setDivergentLevel] = useState(props.divergentLevel);
    const [convergentLevel, setConvergentLevel] = useState(props.convergentLevel);
    const [knowledgeLevel, setKnowledgeLevel] = useState(props.knowledgeLevel);

    const divergentLevelBar = {
        width: `${divergentLevel / 10}%`,
        height: '20px',
        backgroundColor: 'blue',
        borderRadius: '10px',
        transition: 'width 0.3s ease'
    };
    const convergentLevelBar = {
        width: `${convergentLevel / 10}%`,
        height: '20px',
        backgroundColor: 'red',
        borderRadius: '10px',
        transition: 'width 0.3s ease'
    };

    const knowledgeLevelBar = {
        width: `${knowledgeLevel / 10}%`,
        height: '20px',
        backgroundColor: 'green',
        borderRadius: '10px',
        transition: 'width 0.3s ease'
    };

    useEffect(() => {
        setDivergentLevel(props.divergentLevel);
        setConvergentLevel(props.convergentLevel);
        setKnowledgeLevel(props.knowledgeLevel);
    }, [props.divergentLevel, props.convergentLevel, props.knowledgeLevel]);

    return(
        <>
            <div className='studentUI'>
                <div className='topbar'>
                    <img src='images/student_wrap_Btn.png' alt='student_wrap_btn'/>
                    Profile
                </div>
                <div className='studentProfile'>
                    <img src='images/student.png' alt='logo'/>
                    <div className='name'>동건</div>
                    <div className='job'>First-year design students</div>
                </div>
                <div className='barContainer'>
                    <div className='gaugeBar'>
                        <div style={divergentLevelBar} />
                    </div>
                    <div className='gaugeBar'>
                        <div style={convergentLevelBar} />
                    </div>
                    <div className='gaugeBar'>
                        <div style={knowledgeLevelBar} />
                    </div>
                </div>

            </div>
        </>
    )
}