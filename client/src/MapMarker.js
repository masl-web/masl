/* global kakao */
import React, { useEffect, useState } from "react";
import styled from "styled-components";
import { StylesProvider } from "@material-ui/core/styles";
import { BottomNavigation, BottomNavigationAction } from "@material-ui/core";
import LocalCafeIcon from "@material-ui/icons/LocalCafe";
import FastfoodIcon from "@material-ui/icons/Fastfood";
import LocalConvenienceStoreIcon from "@material-ui/icons/LocalConvenienceStore";
import StorefrontIcon from "@material-ui/icons/Storefront";
import LocalGroceryStoreIcon from "@material-ui/icons/LocalGroceryStore";

export default function Map() {
  const [data, setData] = useState({});
  const [isShow, setIsShow] = useState({
    cafe: true,
    fastfood: true,
    convinence: true,
    drugstore: true,
    mart: true,
  });

  //mock data 불러오기
  useEffect(() => {
    fetch("http://localhost:3000/data/areadata.json")
      .then((response) => response.json())
      .then((response) => {
        console.log(response.data);
        setData(response.data);
      });
  }, []);

  useEffect(() => {
    mapscript();
  }, [data]);

  function createMarkerImage(src, size, options) {
    var markerImage = new kakao.maps.MarkerImage(src, size, options);
    return markerImage;
  }

  // function createMarker(position, image) {
  //   var marker = new kakao.maps.Marker({
  //       position: position,
  //       image: image
  //   });
  //   return marker;
  // }

  const createMarker = (map, listName, color, state) => {
    const imageSrc = `/static/image/map-marker_${color}.png`, // 마커이미지의 주소입니다
      imageSize = new kakao.maps.Size(30, 34), // 마커이미지의 크기입니다
      imageOption = { offset: new kakao.maps.Point(27, 69) }; // 마커이미지의 옵션입니다. 마커의 좌표와 일치시킬 이미지 안에서의 좌표를 설정합니다.

    // 마커의 이미지정보를 가지고 있는 마커이미지를 생성합니다
    const markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imageOption);

    if (data[listName] !== undefined) {
      data[listName].forEach((el) => {
        // 마커를 생성합니다
        new kakao.maps.Marker({
          //마커가 표시 될 지도
          map: state ? map : null,
          //마커가 표시 될 위치
          position: new kakao.maps.LatLng(el.lat, el.lng),
          //마커에 hover시 나타날 title
          title: el.store_name,
          //마커 이미지
          image: markerImage,
        });
      });
    }
  };

  const mapscript = () => {
    let container = document.getElementById("map");
    let options = {
      center: new kakao.maps.LatLng(37.50469124951389, 127.04903209973273),
      level: 5,
    };

    //map
    const map = new kakao.maps.Map(container, options);

    createMarker(map, "cafeList", "yellow", isShow.cafe);
    createMarker(map, "convList", "blue", isShow.convinence);
    createMarker(map, "drugList", "orange", isShow.drugstore);
    createMarker(map, "martList", "green", isShow.mart);
    createMarker(map, "fastList", "purple", isShow.fastfood);
  };

  const [value, setValue] = React.useState("cafe");

  const handleChange = (event) => {
    const target = event.target.value;
    console.log(event);
    setIsShow({ ...isShow, [target]: false });
  };

  return (
    <>
      <div id="map" style={{ width: "100vw", height: "100vh" }}></div>
      <StylesProvider injectFirst>
        <MarkerNav showLabels>
          <MarkerNavElement label="카페" value="cafe" icon={<LocalCafeIcon />} className={isShow.cafe ? "Mui-selected" : ""} />
          <MarkerNavElement label="패스트푸드" value="fastfood" icon={<FastfoodIcon />} className={isShow.fastfood ? "Mui-selected" : ""} />
          <MarkerNavElement
            label="편의점"
            value="convinence"
            icon={<LocalConvenienceStoreIcon />}
            className={isShow.convinence ? "Mui-selected" : ""}
            onClick={handleChange}
          />
          <MarkerNavElement
            label="드럭스토어"
            value="drugstore"
            icon={<StorefrontIcon />}
            className={isShow.drugstore ? "Mui-selected" : ""}
          />
          <MarkerNavElement label="마트" value="mart" icon={<LocalGroceryStoreIcon />} className={isShow.mart ? "Mui-selected" : ""} />
        </MarkerNav>
      </StylesProvider>
    </>
  );
}

const MarkerNav = styled(BottomNavigation)`
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 10;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 1rem;
`;

const MarkerNavElement = styled(BottomNavigationAction)`
  .MuiBottomNavigationAction-label {
    font-size: 0.5rem;
  }
  .Mui-selected {
    font-size: 0.7rem;
  }
`;
