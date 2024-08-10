import React from 'react';
import '../chat.css'
import { marked } from 'marked';
import DOMPurify from 'dompurify';

export const ChatBubble = ({speaker, content, mode}) => {

    const createMarkup = () => {
        

        if (typeof content !== 'string') {
            console.error('Expected markdownText to be a string', content);
            return { __html: '' };
        }
      
        try {
            const rawMarkup = marked.parse(content);
            return { __html: DOMPurify.sanitize(rawMarkup) };
          } catch (error) {
            console.error('Error parsing markdown', error);
            return { __html: '' };
          }
      };

    return(
        <>
            {speaker === "student" ? 
                <div className='studentchatHolder'>
                    <img src='images/student.png' alt='logo'/>
                    <div className='studentchat'>
                        <div className='studentName'>동건</div>
                        <div className='chatbubble' dangerouslySetInnerHTML={createMarkup()}/>
                    </div>
                </div>
                :
                <div className='instructorchatHolder'>
                    <div className='userName'>You</div>
                    <div className='instructorchat'>
                        {content}
                    </div>
                </div>
            }
        </>
    )
}