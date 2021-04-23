import React, { useState } from 'react';

import { makeStyles, Grid } from '@material-ui/core';
import Button from '@material-ui/core/Button';
import CloseIcon from '@material-ui/icons/Close';
import CheckIcon from '@material-ui/icons/Check';
import NavBar from './NavBar.js';

var answerList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

const useStyles = makeStyles((theme) => ({
    container: {
        width: '100%',
        maxWidth: '1100px',
        height: '400px',
        padding: '50px',
        margin: '80px auto 80px',
        textAlign: 'center',
        background: '#f4c922',
        borderRadius: '20px',
        boxSizing: 'border-box'
    },
    legend: {
        width: '160px',
        padding: '20px',
        border: '1px solid black',
        background: 'white',
        float: 'right'
    },
    yesBar: {
        width: '60px',
        height: '10px',
        margin: 'auto',
        background: 'green',
        borderRadius: '10px',
        float: 'left'
    },
    noBar: {
        width: '60px',
        height: '10px',
        margin: 'auto',
        background: 'red',
        borderRadius: '10px',
        float: 'left'
    },
    questionBox: {
        width: '400px',
        height: '200px',
        background: 'white',
        margin: 'auto',
        border: '1px solid black',
        lineHeight: '200px'
    },
    yesButton: {
        padding: theme.spacing(1),
        background: "green",
        color: "white"
    },
    noButton: {
        padding: theme.spacing(1),
        background: "red",
        color: "white"
    }
}));

function FlowChart() {
    const questionDict = {
        1: "강남구에 거주하고 있나요?",
        2: "강남구에 살 곳을 찾고 있나요?",
        3: "학생인가요?",
        4: "강남구민의 생활이 궁금한가요?",
        5: "강남구에서 일하고 있나요?",
        6: "강남구를 방문해 본 적이 있나요?",
        7: "일자리를 찾고 있나요?",
        8: "서울시에 거주하고 있나요?",
        9: "결혼을 한 상태인가요?",
        10: "지역사회 활동에 관심이 있나요?"
    }

    const [level, setLevel] = useState(1);
    const [answer, setAnswer] = useState('');
    
    const classes = useStyles();
    
    const onYesQuestion = () =>{
        if (level === 1){
            answerList[level-1] = 1
            setLevel(5);
        } else if (level === 2){
            answerList[level-1] = 1
            setLevel(4);
        } else if (level === 3){
            answerList[level-1] = 1
            setLevel(6);
        } else if (level === 4){
            answerList[level-1] = 1
            setAnswer('E');
        } else if (level === 5){
            answerList[level-1] = 1
            setLevel(9);
        } else if (level === 6){
            answerList[level-1] = 1
            setLevel(8);
        } else if (level === 7){
            answerList[level-1] = 1
            setAnswer('A');
        } else if (level === 8){
            answerList[level-1] = 1
            setAnswer('C');
        } else if (level === 9){
            answerList[level-1] = 1
            setAnswer('B')
        } else if (level === 10){
            answerList[level-1] = 1
            setAnswer('D');
        } 
    };

    const onNoQuestion = () =>{
        if (level === 1){
            setLevel(2);
        } else if (level === 2){
            setLevel(3);
        } else if (level === 3){
            setLevel(5);
        } else if (level === 4){
            setLevel(6);
        } else if (level === 5){
            setLevel(7);
        } else if (level === 6){
            setLevel(10);
        } else if (level === 7){
            setLevel(9);
        } else if (level === 8){
            setLevel(10);
        } else if (level === 9){
            setAnswer('C');
        } else if (level === 10){
            setAnswer('E');
            console.log(answerList);
        } 
    };

  return (
    <>
        <NavBar />
        <Grid className={classes.container}>
            <h1>당신에게 필요한 슬세권 찾기</h1>
            <div className={classes.legend}>
                <div style={{display:'flex'}}>
                    <div className={classes.yesBar}></div>
                    <span style={{fontWeight:'bold'}}>YES</span>
                </div>
                <div style={{display:'flex'}}>
                    <div className={classes.noBar}></div>
                    <span style={{fontWeight:'bold'}}>NO</span>
                </div>
            </div>
            <div className={classes.questionBox}>
                <h1>{answer === "" ? questionDict[level] : ""}</h1>
                <h1>{answer}</h1>
            </div>
            <Button
                  variant="contained"
                  className={classes.yesButton}
                  endIcon={<CheckIcon></CheckIcon>}
                  onClick={onYesQuestion}
                >
                YES
            </Button>
            <Button
                  variant="contained"
                  className={classes.noButton}
                  endIcon={<CloseIcon></CloseIcon>}
                  onClick={onNoQuestion}
                >
                NO
            </Button>
        </Grid>
    </>
  );
}

export default FlowChart;