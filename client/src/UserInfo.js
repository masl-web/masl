import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Redirect, useHistory } from 'react-router';
import { Switch, Route, Link, BrowserRouter as Router } from "react-router-dom";

import { Container, Row, Col, Card, FormControl, Form } from 'react-bootstrap';
import Navbar from 'react-bootstrap/Navbar';
import './App.css';
import { Paper, makeStyles, Grid, TextField } from '@material-ui/core';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import Masl from './Masl';
import { textAlign } from '@material-ui/system';
import AreaDetail from './AreaDetail';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import CheckBoxOutlineBlankIcon from '@material-ui/icons/CheckBoxOutlineBlank';
import CheckBoxIcon from '@material-ui/icons/CheckBox';
import Favorite from '@material-ui/icons/Favorite';
import FavoriteBorder from '@material-ui/icons/FavoriteBorder';

function UserInfo(){

    const history = useHistory();

    const [areaList, setAreaList] = useState();
    const [userInfo, setUserInfo] = useState();
    const [place, setPlace] = useState();
    const handleChangePlace = (e) => {
        setPlace(e.target.value)
    }
    const [cafe, setCafe] = useState();
    const handleChangeCafe = (e) => {
        setCafe(e.target.value)
    }
    const [fastfood, setFastfood] = useState();
    const handleChangeFastfood = (e) => {
        setFastfood(e.target.value)
    }
    const [drug, setDrug] = useState();
    const handleChangeDrug = (e) => {
        setDrug(e.target.value)
    }
    const [convenient, setConvenient] = useState();
    const handleChangeConvenient = (e) => {
        setConvenient(e.target.value)
    }
    const [mart, setMart] = useState();
    const handleChangeMart = (e) => {
        setMart(e.target.value)
    }


    function handleSubmit(){
        const userInfo = {
            address: '서울시 서초구 서초중앙로 65',
            brand: ["스타벅스", "세븐일레븐", "맥도날드"],
            withCredentials: true
        };
        axios.post('http://masl.koreacentral.cloudapp.azure.com:5000/userinfo', userInfo)
        .then(response => setTimeout(()=>{{
            var res = response.data.areaList;
            setAreaList(res);
            history.push({
                pathname:"/masl",
                state: areaList // Masl.js로 데이터 같이 보내주기
            });
        }},75000))
        .catch(function(err){
            console.log("사용자 정보 전송 오류");
        })
    }

    return(
        <Grid>
            <Paper>
                <TextField id="outlined-basic" label="자주 방문하는 주소를 입력해주세요" placeholder="회사 학교 등" variant="outlined"
                    value={place} onChange={handleChangePlace} />
                        <p>☕️ 카페</p>
                        <Form>
                            <Form.Check 
                            type="checkbox"
                            id="starbucks"
                            value="스타벅스"
                            label="스타벅스"
                            />
                            <Form.Check 
                            type="checkbox"
                            id="angelinus"
                            value="엔제리너스"
                            label="엔젤리너스"
                            />
                            <Form.Check 
                            type="checkbox"
                            id="gongcha"
                            value="공차"
                            label="공차"
                            />
                            <Form.Check 
                            type="checkbox"
                            id="coffeebean"
                            value="커피빈"
                            label="커피빈"
                            />
                            <Form.Check 
                            type="checkbox"
                            id="hollys"
                            value="할리스커피"
                            label="할리스커피"
                            />
                            <Form.Check 
                            type="checkbox"
                            id="paulbassett"
                            value="폴바셋"
                            label="폴바셋"
                            />
                            </Form>
                        {/* <p>패스트푸드</p>
                        <FormControl>
                        <input type='checkbox' id='chkok' name='store' value='맥도날드'>맥도날드</input>
                        <input type='checkbox' id='chkok' name='store' value='버거킹'>버거킹</input>
                        <input type='checkbox' id='chkok' name='store' value='서브웨이'>서브웨이</input>
                        <input type='checkbox' id='chkok' name='store' value='롯데리아'>롯데리아</input>
                        <input type='checkbox' id='chkok' name='store' value='이삭토스트'>이삭토스트</input>
                        </FormControl>
                        <p>편의점</p>
                        <FormControl>
                        <input type='checkbox' id='chkok' name='store' value='gs25'>gs25</input>
                        <input type='checkbox' id='chkok' name='store' value='cu'>cu</input>
                        <input type='checkbox' id='chkok' name='store' value='세븐일레븐'>세븐일레븐</input>
                        <input type='checkbox' id='chkok' name='store' value='미니스탑'>미니스탑</input>
                        <input type='checkbox' id='chkok' name='store' value='이마트24'>이마트24</input>
                        </FormControl>
                        <p>드럭스토어</p>
                        <FormControl>
                        <input type='checkbox' id='chkok' name='store' value='올리브영'>올리브영</input>
                        <input type='checkbox' id='chkok' name='store' value='롭스'>롭스</input>
                        <input type='checkbox' id='chkok' name='store' value='랄라블라'>랄라블라</input>
                        </FormControl>
                        <p>마트</p>
                        <FormControl>
                        <input type='checkbox' id='chkok' name='store' value='이마트'>이마트</input>
                        <input type='checkbox' id='chkok' name='store' value='홈플러스'>홈플러스</input>
                        <input type='checkbox' id='chkok' name='store' value='롯데마트'>롯데마트</input>
                        </FormControl> */}
                        <br/>
                            <Button color="primary" onClick={handleSubmit}>마이 슬세권 찾기</Button>
            </Paper>
        </Grid>
    );
}

export default UserInfo;