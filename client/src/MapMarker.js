/*global kakao */
import React, { useEffect, useState } from "react";

export default function Map() {
  const [data, setData] = useState({});

  //mock data 불러오기
  useEffect(() => {
    fetch("http://localhost:3000/data/areadata.json")
    .then((response) => response.json())
    .then((response) => {
      console.log(response.data);
      setData(response.data);
    })
  }, [])

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

  const createMarker = (map, listName, color) => {
    const imageSrc = `/static/image/map-marker_${color}.png`, // 마커이미지의 주소입니다    
    imageSize = new kakao.maps.Size(30, 34), // 마커이미지의 크기입니다
    imageOption = {offset: new kakao.maps.Point(27, 69)}; // 마커이미지의 옵션입니다. 마커의 좌표와 일치시킬 이미지 안에서의 좌표를 설정합니다.
  
    // 마커의 이미지정보를 가지고 있는 마커이미지를 생성합니다
    const markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imageOption)

    if (data[listName] !== undefined) {
      data[listName].forEach((el) => {
          // 마커를 생성합니다
          new kakao.maps.Marker({
          //마커가 표시 될 지도
          map: map,
          //마커가 표시 될 위치
          position: new kakao.maps.LatLng(el.lat, el.lng),
          //마커에 hover시 나타날 title
          title: el.store_name,
          //마커 이미지
          image: markerImage
        });
      });
    }
  }

  const mapscript = () => {
    let container = document.getElementById("map");
    let options = {
      center: new kakao.maps.LatLng(37.50469124951389, 127.04903209973273),
      level: 5,
    };

    //map
    const map = new kakao.maps.Map(container, options);

    createMarker(map, "cafeList", "yellow");
    createMarker(map, "convList", "blue");
    createMarker(map, "drugList", "orange");
    createMarker(map, "martList", "green");
    createMarker(map, "fastList", "purple");
  };


  return <div id="map" style={{ width: "100vw", height: "100vh" }}></div>;
}
