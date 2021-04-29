/*global kakao */
import React, { useEffect, useState } from "react";

export default function Map() {
  const [markerData, setMarkerData] = useState([]);

  //mock data 불러오기
  useEffect(() => {
    fetch("http://localhost:3000/data/areadata.json")
    .then((response) => response.json())
    .then((response) => {
      console.log(response.areaList);
      setMarkerData(response.areaList);
    }); 
  }, [])

  useEffect(() => {
    mapscript();
  }, [markerData]);

  const mapscript = () => {
    let container = document.getElementById("map");
    let options = {
      center: new kakao.maps.LatLng(37.50469124951389, 127.04903209973273),
      level: 5,
    };

    //map
    const map = new kakao.maps.Map(container, options);

    markerData.forEach((el) => {
      console.log(el);
      // 마커를 생성합니다
      new kakao.maps.Marker({
        //마커가 표시 될 지도
        map: map,
        //마커가 표시 될 위치
        position: new kakao.maps.LatLng(el.lat, el.lng),
        //마커에 hover시 나타날 title
        title: el.store_name,
      });
    });
  };


  return <div id="map" style={{ width: "100vw", height: "100vh" }}></div>;
}
