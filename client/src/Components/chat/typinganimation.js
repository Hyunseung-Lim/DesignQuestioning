import React, { useState, useEffect } from 'react';

export const TypingAnimation = ({ interval = 500, isDisable ,reset }) => {
    const [displayText, setDisplayText] = useState('');
    const [index, setIndex] = useState(0);
    const outputs = ['음...그게.........', '어...그니까요........', '그건...말이죠.........'];

    // Function to get a random output
    const getRandomOutput = () => {
        const randomIndex = Math.floor(Math.random() * outputs.length);
        return outputs[randomIndex];
    };

    useEffect(() => {
        let typingInterval;
        let text = getRandomOutput();

        if (isDisable) {
            typingInterval = setInterval(() => {
                setIndex(prevIndex => {
                    if (prevIndex < text.length) {
                        setDisplayText(text.substring(0, prevIndex + 1));
                        return prevIndex + 1;
                    } else {
                        // Reset to start the animation again
                        setDisplayText('');
                        return 0;
                    }
                });
            }, interval);
        }

        return () => {
            clearInterval(typingInterval);
            setDisplayText(''); // Reset the display text when stopping
            setIndex(0);        // Reset the index when stopping
        };
    }, [isDisable, interval]);

    useEffect(() => {
        if (reset) {
            setDisplayText('');
            setIndex(0);
        }
    }, [reset]);

    return <div>{displayText}</div>;
};