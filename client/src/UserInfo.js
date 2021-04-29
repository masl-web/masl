import React, { useEffect, useState } from "react";
import axios from "axios";
import { Redirect, useHistory } from "react-router";
import { Switch, Route, Link, BrowserRouter as Router } from "react-router-dom";

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
import Checkbox from "@material-ui/core/Checkbox";
import CheckBoxOutlineBlankIcon from "@material-ui/icons/CheckBoxOutlineBlank";
import CheckBoxIcon from "@material-ui/icons/CheckBox";
import Favorite from "@material-ui/icons/Favorite";
import FavoriteBorder from "@material-ui/icons/FavoriteBorder";

import Masl from "./Masl";
import ModalAddress from "./ModalAddress";

function Cafe({ index, cafe, checkedCafeHandler }) {
  const [bChecked, setChecked] = useState(false);
  function checkHandler(e) {
    setChecked(!bChecked);
    console.log(index);
    checkedCafeHandler(index, cafe, e.target.checked);
  }
  return (
    <>
      <input type="checkbox" checked={bChecked} onChange={checkHandler} />
      {cafe}
    </>
  );
}

function CafeList({ setUserCafe }) {
  const cafes = [
    "스타벅스",
    "폴바셋",
    "엔제리너스",
    "할리스",
    "커피빈",
    "공차",
  ];
  const [checkedCafes, setCheckedCafes] = useState(new Set());
  const checkedCafeHandler = (id, cafe, isChecked) => {
    if (isChecked) {
      checkedCafes.add(cafe);
      setCheckedCafes(checkedCafes);
      setUserCafe(checkedCafes);
    } else if (!isChecked && checkedCafes.has(cafe)) {
      checkedCafes.delete(cafe);
      setCheckedCafes(checkedCafes);
      setUserCafe(checkedCafes);
    }
    console.log(checkedCafes);
  };

  return (
    <>
      {cafes.map((cafe, index) => (
        <Cafe
          key={index}
          cafe={cafe}
          index={index}
          checkedCafeHandler={checkedCafeHandler}
        />
      ))}
    </>
  );
}

function Fastfood({ index, fastfood, checkedFastfoodHandler }) {
  const [bChecked, setChecked] = useState(false);
  function checkHandler(e) {
    setChecked(!bChecked);
    console.log(index);
    checkedFastfoodHandler(index, fastfood, e.target.checked);
  }
  return (
    <>
      <input type="checkbox" checked={bChecked} onChange={checkHandler} />
      {fastfood}
    </>
  );
}

function FastfoodList({ setUserFastfood }) {
  const fastfoods = [
    "맥도날드",
    "롯데리아",
    "버거킹",
    "서브웨이",
    "이삭토스트",
  ];
  const [checkedFastfoods, setCheckedFastfoods] = useState(new Set());
  const checkedFastfoodHandler = (id, fastfood, isChecked) => {
    if (isChecked) {
      checkedFastfoods.add(fastfood);
      setCheckedFastfoods(checkedFastfoods);
      setUserFastfood(checkedFastfoods);
    } else if (!isChecked && checkedFastfoods.has(fastfood)) {
      checkedFastfoods.delete(fastfood);
      setCheckedFastfoods(checkedFastfoods);
      setUserFastfood(checkedFastfoods);
    }
    console.log(checkedFastfoods);
  };

  return (
    <>
      {fastfoods.map((fastfood, index) => (
        <Fastfood
          key={index}
          fastfood={fastfood}
          index={index}
          checkedFastfoodHandler={checkedFastfoodHandler}
        />
      ))}
    </>
  );
}

function Convenience({ index, convenience, checkedConvenienceHandler }) {
  const [bChecked, setChecked] = useState(false);
  function checkHandler(e) {
    setChecked(!bChecked);
    console.log(index);
    checkedConvenienceHandler(index, convenience, e.target.checked);
  }
  return (
    <>
      <input type="checkbox" checked={bChecked} onChange={checkHandler} />
      {convenience}
    </>
  );
}

function ConvenienceList({ setUserConvenience }) {
  const conveniences = ["GS25", "CU", "세븐일레븐", "미니스톱", "이마트24"];
  const [checkedConveniences, setCheckedConveniences] = useState(new Set());
  const checkedConvenienceHandler = (id, convenience, isChecked) => {
    if (isChecked) {
      checkedConveniences.add(convenience);
      setCheckedConveniences(checkedConveniences);
      setUserConvenience(checkedConveniences);
    } else if (!isChecked && checkedConveniences.has(convenience)) {
      checkedConveniences.delete(convenience);
      setCheckedConveniences(checkedConveniences);
      setUserConvenience(checkedConveniences);
    }
    console.log(checkedConveniences);
  };

  return (
    <>
      {conveniences.map((convenience, index) => (
        <Convenience
          key={index}
          convenience={convenience}
          index={index}
          checkedConvenienceHandler={checkedConvenienceHandler}
        />
      ))}
    </>
  );
}

function Drugstore({ index, drugstore, checkedDrugstoreHandler }) {
  const [bChecked, setChecked] = useState(false);
  function checkHandler(e) {
    setChecked(!bChecked);
    console.log(index);
    checkedDrugstoreHandler(index, drugstore, e.target.checked);
  }
  return (
    <>
      <input type="checkbox" checked={bChecked} onChange={checkHandler} />
      {drugstore}
    </>
  );
}

function DrugstoreList({ setUserDrugstore }) {
  const drugstores = ["올리브영", "롭스", "랄라블라"];
  const [checkedDrugstores, setCheckedDrugstores] = useState(new Set());
  const checkedDrugstoreHandler = (id, drugstore, isChecked) => {
    if (isChecked) {
      checkedDrugstores.add(drugstore);
      setCheckedDrugstores(checkedDrugstores);
      setUserDrugstore(checkedDrugstores);
    } else if (!isChecked && checkedDrugstores.has(drugstore)) {
      checkedDrugstores.delete(drugstore);
      setCheckedDrugstores(checkedDrugstores);
      setUserDrugstore(checkedDrugstores);
    }
    console.log(checkedDrugstores);
  };

  return (
    <>
      {drugstores.map((drugstore, index) => (
        <Drugstore
          key={index}
          drugstore={drugstore}
          index={index}
          checkedDrugstoreHandler={checkedDrugstoreHandler}
        />
      ))}
    </>
  );
}

function Mart({ index, mart, checkedMartHandler }) {
  const [bChecked, setChecked] = useState(false);
  function checkHandler(e) {
    setChecked(!bChecked);
    console.log(index);
    checkedMartHandler(index, mart, e.target.checked);
  }
  return (
    <>
      <input type="checkbox" checked={bChecked} onChange={checkHandler} />
      {mart}
    </>
  );
}

function MartList({ setUserMart }) {
  const marts = ["이마트", "홈플러스", "롯데마트"];
  const [checkedMarts, setCheckedMarts] = useState(new Set());
  const checkedMartHandler = (id, mart, isChecked) => {
    if (isChecked) {
      checkedMarts.add(mart);
      setCheckedMarts(checkedMarts);
      setUserMart(checkedMarts);
    } else if (!isChecked && checkedMarts.has(mart)) {
      checkedMarts.delete(mart);
      setCheckedMarts(checkedMarts);
      setUserMart(checkedMarts);
    }
    console.log(checkedMarts);
  };

  return (
    <>
      {marts.map((mart, index) => (
        <Mart
          key={index}
          mart={mart}
          index={index}
          checkedMartHandler={checkedMartHandler}
        />
      ))}
    </>
  );
}

function UserInfo() {
  const history = useHistory();

  const [areaList, setAreaList] = useState();

  const [modalOpen, setModalOpen] = useState(false);

  const [address, setAddress] = useState(null);
  const [userCafe, setUserCafe] = useState(new Set());
  const [userFastfood, setUserFastfood] = useState(new Set());
  const [userDrugstore, setUserDrugstore] = useState(new Set());
  const [userConvenience, setUserConvenience] = useState(new Set());
  const [userMart, setUserMart] = useState(new Set());
  /* code by 성민 */
  const openModal = () => {
    setModalOpen(true);
  };
  const closeModal = () => {
    setModalOpen(false);
  };

  function handleSubmit(e) {
    e.preventDefault();
    const brand = [
      ...Array.from(userCafe),
      ...Array.from(userFastfood),
      ...Array.from(userDrugstore),
      ...Array.from(userConvenience),
      ...Array.from(userMart),
    ];

    console.log(brand);
    var userInfo = {
      address: address,
      brand: brand,
    };
    axios
      .post("http://localhost:5000/userinfo", userInfo)
      .then((response) => {
        var res = response.data.areaList;
        setAreaList(res);
        console.log(areaList);
        history.push({
          pathname: "/masl",
          state: areaList, // Masl.js로 데이터 같이 보내주기
        });
      })
      .catch(function (err) {
        console.log("사용자 정보 전송 오류");
      });
  }

  return (
    <>
      {/* code by 성민 */}
      <Row>
        <Form>
          <Form.Control
            placeholder="자주 가는 주소를 입력해주세요"
            onFocus={openModal}
          />
        </Form>
        <ModalAddress
          open={modalOpen}
          closeModal={closeModal}
          address={address}
          setAddress={() => {
            setAddress();
          }}
          header="자주 가는 곳이 어디신가요?"
        />
      </Row>
      <Form onSubmit={handleSubmit}>
        <p>카페</p>
        <CafeList setUserCafe={setUserCafe} />
        <p>패스트푸드</p>
        <FastfoodList setUserFastfood={setUserFastfood} />
        <p>편의점</p>
        <ConvenienceList setUserConvenience={setUserConvenience} />
        <p>드럭스토어</p>
        <DrugstoreList setUserDrugstore={setUserDrugstore} />
        <p>마트</p>
        <MartList setUserMart={setUserMart} />
        <button type="submit">찾기</button>
      </Form>
    </>
  );
}

export default UserInfo;
