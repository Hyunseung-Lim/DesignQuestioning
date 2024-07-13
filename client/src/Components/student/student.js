import React, {useState, useEffect} from 'react';
import './student.css'
import { RadarChart } from '../radar/RadarChart';

export const Student = (props) => {

    const [totalExp, setTotalExp] = useState(0);
    const [studentLevel, setStudentLevel] = useState(1);
    const [currentExp, setCurrentExp] = useState(0);
    const [animate, setAnimate] = useState(true);
    const maxExp = 100;
    const [userTab, setUserTab] = useState(false);

    const radardata = {
        labels: [
            'Eating',
            'Drinking',
            'Sleeping',
            'Designing',
            'Coding',
            'Cycling',
            'Running'
        ],
        datasets: [{
            label: 'My First Dataset',
            data: [65, 59, 90, 81, 56, 55, 40],
            fill: true,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgb(255, 99, 132)',
            pointBackgroundColor: 'rgb(255, 99, 132)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(255, 99, 132)'
        }, {
            label: 'My Second Dataset',
            data: [28, 48, 40, 19, 96, 27, 100],
            fill: true,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgb(54, 162, 235)',
            pointBackgroundColor: 'rgb(54, 162, 235)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(54, 162, 235)'
        }]
    };

    // const [divergentLevel, setDivergentLevel] = useState(props.divergentLevel);
    // const [convergentLevel, setConvergentLevel] = useState(props.convergentLevel);
    // const [knowledgeLevel, setKnowledgeLevel] = useState(props.knowledgeLevel);

    // const expBar = {
    //     width: `${currentExp}%`,
    //     height: '20px',
    //     backgroundColor: '#12CCAE',
    //     borderRadius: '10px',
    //     transition: 'width 0.3s ease'
    // };

    function userTabChange (i) {
        setUserTab(i);
    }

    useEffect(() => {
        if ((currentExp + props.knowledgeLevel - totalExp) >= maxExp) {
            setCurrentExp(maxExp); // Temporarily set to max for visual effect
            setAnimate(false); // Disable animation for reset

            setTimeout(() => {
                const excessExp = currentExp + props.knowledgeLevel - totalExp - maxExp;
                let newLevel = studentLevel;
                let newExp = excessExp;

                // Check if the excess experience is enough to level up multiple times
                while (newExp >= maxExp) {
                    newLevel += 1;
                    newExp -= maxExp;
                }

                setStudentLevel(newLevel + 1);
                setCurrentExp(newExp);
                setAnimate(true); // Re-enable animation
            }, 300); // Delay for the animation, 1000 ms or 1 second
        }
        else {
            setCurrentExp(currentExp + props.knowledgeLevel - totalExp);
        }
        setTotalExp(props.knowledgeLevel);
    }, [props.knowledgeLevel]);

    return(
        <>
            <div className='studentUI'>
                {/* <div className='topbar'>
                    <img src='images/student_wrap_Btn.png' alt='student_wrap_btn'/>
                </div> */}
                <div className='title'>학생(동건) 프로필</div>
                <div className='studentProfile'>
                    <img src='images/student.png' alt='logo'/>
                    <div className= 'barContainer'>
                        <div className={animate ? 'gague' : 'gague no-animation'} style={{ width: `${currentExp}%` }}/>
                    </div>
                    <div className='levelContainer'>
                        <div className='level'>Level {studentLevel}</div>
                        <div className='exp'>{currentExp} exp points</div>
                    </div>
                </div>
                <div className='title'>사용자 프로필</div>
                <div className='buttonContainer'>
                    <button className={userTab ? 'userBtn clicked' : 'userBtn'} onClick={() => userTabChange(true)}>프로필</button>
                    <button className={userTab ? 'userBtn' : 'userBtn clicked'} onClick={() => userTabChange(false)}>피드백</button>
                </div>
                <div className='userStatus'>
                    {userTab ?
                        <div></div>
                        :
                        <div className='radar'>
                            <RadarChart/>
                        </div>
                    }
                </div>
            </div>
        </>
    )
}