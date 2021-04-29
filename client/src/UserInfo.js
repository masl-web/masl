import React, { useEffect, useState } from "react";
import axios from "axios";
import { Redirect, useHistory } from "react-router";
import { Switch, Route, Link, BrowserRouter as Router } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux"

import { Container, Row, Col, Card, FormControl, Form } from "react-bootstrap";
import Navbar from "react-bootstrap/Navbar";

import { Paper, makeStyles, Grid, TextField } from "@material-ui/core";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import IconButton from "@material-ui/core/IconButton";
import { textAlign } from "@material-ui/system";
import AreaDetail from "./AreaDetail";
import FormGroup from "@material-ui/core/FormGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import CheckBoxOutlineBlankIcon from "@material-ui/icons/CheckBoxOutlineBlank";
import CheckBoxIcon from "@material-ui/icons/CheckBox";
import Favorite from "@material-ui/icons/Favorite";
import FavoriteBorder from "@material-ui/icons/FavoriteBorder";

import "./App.css";
import Masl from "./Masl";
import ModalAddress from "./ModalAddress";
import './UserInfo.css';
import { addBrand, removeBrand } from './actions'

function Checkbox({ id, name, image }) {
    const [isChecked, setIsChecked] = useState(false);
  
    function checkHandler() {
        setIsChecked(!isChecked)
    } 
  
    return (
        <div className="checkbox-form">
          <input type="checkbox" id={id} name={name} checked={isChecked} onChange={checkHandler} />
          <label htmlFor={id}>
            <div className="chk_img">
              <img src={image} alt={name} />
            </div>
          </label>
        </div>
    );
  }

function CheckboxList({ id, data }) {
    const dispatch = useDispatch();     
  
    function listChangeHandler(e) {
      console.log(e.target.name, e.target.checked);
  
      if (e.target.checked) {
        dispatch(addBrand(e.target.name));
      } else {
        dispatch(removeBrand(e.target.name));
      }
    }
  
    return (
      <>
        <div id={id} onChange={listChangeHandler}>
            {data.map((brand, index) => (
                <Checkbox key={index} id={brand.id} name={brand.name} image={brand.image} />
            ))}
        </div>
      </>
    );
  }

  const cafes = [
    {
      id: "c1",
      name: "starbucks",
      image: "./images/starbucks_logo.png",
    },
    {
      id: "c2",
      name: "paulbassett",
      image: "./images/paulbassett_logo.png",
    },
    {
      id: "c3",
      name: "angelinus",
      image: "./images/angelinus_logo.png",
    },
    {
      id: "c4",
      name: "hollys",
      image: "./images/hollys_logo.png",
    },
    {
      id: "c5",
      name: "coffeebin",
      image: "./images/coffeebin_logo.png",
    },
    {
      id: "c6",
      name: "gongcha",
      image: "./images/gongcha_logo.png",
    },
  ]; 
  const fastfoods = [
    {
      id: "f1",
      name: "mcdonalds",
      image: "./images/mcdonalds_logo.png",
    },
    {
      id: "f2",
      name: "lotteria",
      image: "./images/lotteria_logo.png",
    },
    {
      id: "f3",
      name: "burgerking",
      image: "./images/burgerking_logo.png",
    },
    {
      id: "f4",
      name: "subway",
      image: "./images/subway_logo.png",
    },
    {
      id: "f5",
      name: "isaactost",
      image: "./images/isaactoast_logo.png",
    },
  ];
  const conveniences = [
    {
      id: "v1",
      name: "gs25",
      image: "./images/gs25_logo.png",
    },
    {
      id: "v2",
      name: "cu",
      image: "./images/cu_logo.png",
    },
    {
      id: "v3",
      name: "7eleven",
      image: "./images/7eleven_logo.png",
    },
    {
      id: "v4",
      name: "ministop",
      image: "./images/ministop_logo.png",
    },
    {
      id: "v5",
      name: "emart24",
      image: "./images/emart24_logo.png",
    },
  ];
  const drugstores = [
    {
      id: "d1",
      name: "oliveyoung",
      image: "./images/oliveyoung_logo.png",
    },
    {
      id: "d2",
      name: "lohbs",
      image: "./images/lohbs_logo.png",
    },
    {
      id: "d3",
      name: "lalavla",
      image: "./images/lalavla_logo.png",
    },
  ];
  const marts = [
    {
      id: "m1",
      name: "emart",
      image: "./images/emart_logo.png",
    },
    {
      id: "m2",
      name: "homeplus",
      image: "./images/homeplus_logo.png",
    },
    {
      id: "m3",
      name: "lottemart",
      image: "./images/lottemart_logo.png",
    },
  ];

function UserInfo() {
    const history = useHistory();
    const userInfo = useSelector((state)=> state.userInfo);
    const [areaList, setAreaList] = useState();
    const [ modalOpen, setModalOpen ] = useState(false);
    const [address, setAddress] = useState(null);

    /* code by 성민 */
    const openModal = () => {
        setModalOpen(true);
    }
    const closeModal = () => {
        setModalOpen(false);
    }          
    // const userInfo = {
    //     address: userAddress,
    //     brand: checkedBrand
    // };
    // axios.post('http://localhost:5000/userinfo', userInfo)
    // .then(response => {
    //     var res = response.data.areaList;
    //     setAreaList(res);
    //     console.log(areaList);
    //     history.push({
    //         pathname:"/masl",
    //         state: areaList // Masl.js로 데이터 같이 보내주기
    //     });
    // })
    // .catch(function(err){
    //     console.log("사용자 정보 전송 오류");
    // })
    
    return (
    <Container>
      <div>
        <h1>MASL</h1>
        <hr />
        <Row>
         <Form>
            <Form.Control 
              placeholder="자주 가는 주소를 입력해주세요"
              onFocus={ openModal } />
         </Form>
         <ModalAddress 
            open={ modalOpen } 
            closeModal={ closeModal } 
            address={userInfo.address} 
            setAddress={()=>{setAddress();}} 
            header="자주 가는 곳이 어디신가요?"
        />
       </Row>
        {/* code by 성민 */}
      </div>
    <Form className="survey-form">
      <div className="category-form">
      <h4>카페</h4>
      <CheckboxList id="cafe" data={cafes}/>
      </div>
      <div className="category-form">
      <h4>패스트푸드</h4>
      <CheckboxList id="fastfood" data={fastfoods}/>
      </div>
      <div className="category-form">
      <h4>편의점</h4>
      <CheckboxList id="convenience" data={conveniences}/>
      </div>
      <div className="category-form">
      <h4>드럭스토어</h4>
      <CheckboxList id="drugstore" data={drugstores}/>
      </div>
      <div className="category-form">
      <h4>마트</h4>
      <CheckboxList id="mart" data={marts}/>
      </div>
    </Form>
    <Row>
    <hr />
    <Button variant="outlined" onClick={(e)=>{
      e.preventDefault();
      console.log(userInfo)
    }}>찾기</Button>
    <hr />
    </Row>
    </Container>
    );
}

export default UserInfo;
