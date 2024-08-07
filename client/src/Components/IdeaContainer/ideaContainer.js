import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./ideaContainer.css";

export const IdeaContainer = (props) => {
  const [idea, setIdea] = useState(props.ideaData);
  const [currentDescription, setCurrentDescription] = useState(0);
  const [error, setError] = useState(null);
  const buttonRef = useRef(null);
  const popoverRef = useRef(null);

  const ChangeDescription = (i) => {
    if (currentDescription !== i) {
      setCurrentDescription(i);
    }
  };

  const updateIdea = async () => {
    props.setIsUpdateIdea(true);
    await axios({
      method: "GET",
      url: "/updateIdea",
      headers: {
        Authorization: "Bearer " + props.token,
      },
    })
      .then((response) => {
        const res = response.data;
        console.log(res);
        if (res.response === "No action plan to update the idea.") {
          setError(
            "아직 아이디어를 업데이트 하기 위한 충분한 피드백을 받지 못했어요. 대화를 더 진행해주세요."
          );
        } else {
          setError(null);
          props.setIdeaData(res.ideaData);
        }
        props.setIsUpdateIdea(false);
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
        setError("업데이트 중 오류가 발생했습니다.");
        props.setIsUpdateIdea(false);
      });
  };

  const handleClickOutside = (event) => {
    if (
      popoverRef.current &&
      !popoverRef.current.contains(event.target) &&
      !buttonRef.current.contains(event.target)
    ) {
      setError(null);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  useEffect(() => {
    setIdea(props.ideaData);
  }, [props.ideaData]);

  return (
    <>
      <div className="ideaContainerUI">
        <div className="navbar">
          <button
            className={currentDescription === 1 ? "current Tag" : "Tag"}
            onClick={() => ChangeDescription(0)}
          >
            Topic
          </button>
          <button
            className={currentDescription === 0 ? "current right Tag" : "right Tag"}
            onClick={() => ChangeDescription(1)}
          >
            Design Goals
          </button>
        </div>
        <div className="ideaDescription">
          {currentDescription === 0 ? (
            <div className="topic">{idea.topic}</div>
          ) : (
            <div className="goalsConatiner">
              <div className="design_goal">
                <b>Inovation:</b> 아이디어가 얼마나 혁신적인 지
              </div>
              <div className="design_goal">
                <b>Elaboration:</b> 아이디어가 얼마나 정교한지
              </div>
              <div className="design_goal">
                <b>Usability:</b> 아이디어가 얼마나 사용하기 용이한지
              </div>
              <div className="design_goal">
                <b>Value:</b> 아이디어가 얼마나 사용할 가치가 있는지
              </div>
              <div className="design_goal">
                <b>Social Responsiblity:</b> 아이디어가 얼마나 사회적 책임을 이행하는지
              </div>
            </div>
          )}
        </div>
        <div className="ideaContainer">
          <div className={props.isUpdateIdea ? "ideaBox disable" : "ideaBox"}>
            <div className="ideatitle">
              <div className="title">{idea.title}</div>

              <button ref={buttonRef} onClick={updateIdea} disabled={props.isUpdateIdea}>
                Update Idea
              </button>
              {error && (
                <div
                  ref={popoverRef}
                  className="error-popover"
                  style={{
                    top: buttonRef.current.offsetTop + 36,
                    left: buttonRef.current.offsetLeft - 200,
                  }}
                >
                  {error}
                </div>
              )}
            </div>
            <div className="subtitle">Target Problem</div>
            <div className="problem">{idea.problem}</div>
            <div className="subtitle">Idea</div>
            <div className="idea">{idea.idea}</div>
          </div>
        </div>
      </div>
    </>
  );
};
