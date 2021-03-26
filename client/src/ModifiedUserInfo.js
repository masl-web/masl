import React from "react";
import CheckboxList from './CheckBoxComponent';

import './App.css';

function UserInfo() {
  const cafes = ["스타벅스", "폴바셋", "엔제리너스", "할리스", "커피빈", "공차"];
  const fastfoods = ["맥도날드", "롯데리아", "버거킹", "서브웨이", "이삭토스트"];
  const conveniences = ["GS25", "CU", "세븐일레븐", "미니스톱", "이마트24"];
  const drugstores = ["올리브영", "롭스", "랄라블라"];
  const marts = ["이마트", "홈플러스", "롯데마트"];

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
    <form onSubmit={(e)=>{
      e.preventDefault();
      console.log("!!!");
      console.log(getUserInfo());
    }}>
      <h4>카페</h4>
      <CheckboxList id="cafe" data={cafes} />
      <h4>패스트푸드</h4>
      <CheckboxList id="fastfood" data={fastfoods}/>
      <h4>편의점</h4>
      <CheckboxList id="convenience" data={conveniences}/>
      <h4>드럭스토어</h4>
      <CheckboxList id="drugstore" data={drugstores}/>
      <h4>마트</h4>
      <CheckboxList id="mart" data={marts}/>

      <button type="submit">찾기</button>
    </form>
  );
}

export default UserInfo;