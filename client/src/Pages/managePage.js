import React, { useState } from 'react';
import axios from "axios";
import './pages.css'

export const ManagePage = (props) => {

    const [userNum, setUserNum] = useState(0);
    const [state, setState] = useState("No Request");
    const [logData, setLogData] = useState([]);

    const userNumChnage = (event) => {
        setUserNum(event.target.value);
    };

    function flattenObject(obj) {
        const result = {};
    
        for (const key in obj) {
            if (typeof obj[key] === 'object' && obj[key] !== null) {
                const flatObject = flattenObject(obj[key]);
                for (const x in flatObject) {
                    result[key + '.' + x] = flatObject[x];
                }
            } else {
                result[key] = obj[key];
            }
        }
    
        return result;
    }
    
    function convertToCSV(objArray) {
        const array = objArray.map(item => flattenObject(item));
        let str = '';
    
        // Extract headers
        const headers = Object.keys(array[0]);
        str += headers.join(',') + '\r\n';
      
        // Extract data
        for (let i = 0; i < array.length; i++) {
            let line = '';
            for (let index in headers) {
                if (line !== '') line += ',';
                line += '"' + String(array[i][headers[index]]).replace(/"/g, '""') + '"';
            }
            str += line + '\r\n';
        }
    
        return str;
    }    

    const getLogData = async (feedback) => {
        setState("downloading...");
        await axios({
            method: "POST",
            url: "/getLogData",
            headers: {
                Authorization: "Bearer " + props.token,
          },
          data: { userNum: userNum },
        })
        .then((response) => {
        const res = response.data;
            // setLogData(res.logData);
            // console.log(res.logData);
            const csv = convertToCSV(res.logData);
            downloadCSV(csv, "P" +userNum + ".csv");
            setState("P" +userNum + " Done.");
        })
        .catch((error) => {
        if (error.response) {
            console.log(error.response);
            console.log(error.response.status);
            console.log(error.response.headers);
        }
        });
    };

    function downloadCSV(csv, filename) {
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    // function download() {
    //     const csv = convertToCSV(logData);
    //     downloadCSV(csv, "P" +userNum + ".csv");
    // }

    return(
            <div className='managepage'>
                <input onChange={userNumChnage} value={userNum}/>
                <div>state: {state}</div>
                <button onClick={getLogData}>Download</button>
            </div>
    )
}