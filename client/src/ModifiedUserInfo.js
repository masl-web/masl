import React, { useState } from "react";
import { Container, Row, Form } from "react-bootstrap";
import Button from '@material-ui/core/Button';
import './ModifiedUserInfo.css';

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
  const [checkedBrands, setCheckedBrands] = useState([]);

  function listChangeHandler(e) {
    console.log(e.target.name, e.target.checked);

    if (e.target.checked) {
      setCheckedBrands([...checkedBrands, e.target.name]);
    } else {
      const newList = [...checkedBrands].filter(brand => brand !== e.target.name);
      setCheckedBrands(newList);
    }
    // console.log(checkedCafes);
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



function UserInfo() {
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
  

  // redux로 바꿀 예정
  function getUserInfo() {
    const UserInfo = {
      'cafe': [],
      'fastfood': [],
      'convenience': [],
      'drugstore': [],
      'mart': []
    }
    document.getElementById("cafe").querySelectorAll("input:checked").forEach((x)=>{UserInfo['cafe'].push(x.name)});
    document.getElementById("fastfood").querySelectorAll("input:checked").forEach((x)=>{UserInfo['fastfood'].push(x.name)});
    document.getElementById("convenience").querySelectorAll("input:checked").forEach((x)=>{UserInfo['convenience'].push(x.name)});
    document.getElementById("drugstore").querySelectorAll("input:checked").forEach((x)=>{UserInfo['drugstore'].push(x.name)});
    document.getElementById("mart").querySelectorAll("input:checked").forEach((x)=>{UserInfo['mart'].push(x.name)});
    return UserInfo
  }

  return (
    <Container>
      <div>
        <h1>MASL</h1>
        <hr />
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
      console.log("!!!");
      console.log(getUserInfo());
    }}>찾기</Button>
    <hr />
    </Row>
    </Container>
  );
}

export default UserInfo;

// code by 박정환, 윤맑은이슬