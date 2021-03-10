/*global kakao*/
import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router';
import axios from 'axios';

import { Container } from 'react-bootstrap';

const { kakao } = window;

function Masl(props){

    const history = useHistory();
    // default areaList 설정
    const [areaList, setAreaList] = useState();
    const [container, setContainer] = useState();
    const [circles, setCircles] = useState();
    const [circleId, setCircleId] = useState();

    // 페이지 로딩될 때 areaList 받아오기
    useEffect(() => {
        var data = props.location.state;
        setAreaList(data);
    }, []);

    var mainMap = null;

    // areaList가 존재할 때 지도를 띄우기
    useEffect(() => {
        if(!areaList) return
            var container = document.getElementById('map'), // 지도를 표시할 div 
                option = {
                    center: new kakao.maps.LatLng(37.5271186202883, 126.9815088218937), // 지도의 Default 중심좌표
                    level: 8 // 지도의 확대 레벨 
                };
            setContainer(container);
            console.log("컨테이너"); // 찍힘
            mainMap = (new kakao.maps.Map(container, option)); // 지도 생성
            console.log("지도"); // 찍힘
            // 마커(동심원) 그리는 함수 호출하여 반환된 circles 배열을 다시 할당
            var circles_result = drawCircle(areaList);
            setCircles(circles_result);
            
    }, [areaList])

    // circles 가 존재할 때만 지도를 띄우기
    useEffect(() => {
        if(!circles) return
            // 마커(동심원)별 클릭 이벤트 등록
            selectCircle(circles);
            console.log("동심원별 클릭이벤트");
    }, [circles])

    function drawCircle(areaList) { // 마커(동심원) 그리는 함수

        var imageSrc = "/static/image/circle_1.png", // 마커 이미지(동심원)의 주소
            imageSize = new kakao.maps.Size(80, 80), // 마커 이미지의 크기
            imageOption = { offset: new kakao.maps.Point(40, 40) }; // 마커 이미지의 옵션

        var circles_list = []; // 5개의 마커(동심원) 객체를 저장할 배열

        console.log(areaList);
        for (var i = 0; i < areaList.length; i++) { // areaList에 있는 TOP5영역 수만큼 반복하여 마커(동심원) 객체 생성

            var lat_center = areaList[i].lat,
                lng_center = areaList[i].lng;

            var circleImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imageOption), //마커(동심원) 이미지 적용
                circlePosition = new kakao.maps.LatLng(lat_center, lng_center); // 마커(동심원)가 표시될 위치

            // 마커(동심원) 객체 생성 - 임시 변수 tmp_circle 로 매번 마커 객체 1개를 받아서 circles 배열에 저장하는 방식
            var tmp_circle = new kakao.maps.Marker({
                position: circlePosition,
                image: circleImage,
                title: areaList[i].id // 아이디값을 넘겨줌 - 지역별 매장 리스트 불러오기 위해
            });

            circles_list.push(tmp_circle); //.append() 와 같은 역할
        }
        // 현재 지도에 동심원들 그리기
        for (var i = 0; i < circles_list.length; i++) {
            circles_list[i].setMap(mainMap);
        }

        return (circles_list); // 5개의 마커(동심원) 객체 배열 반환
    }

    function selectCircle(circles) { // 마커(동심원)별 클릭 이벤트 등록하는 함수 - 특정 지역을 선택했을 떄 해당 지역의 정보를 백엔드로 보내야 함

        kakao.maps.event.addListener(circles[0], 'click', function () { // 마커(동심원)의 좌표에 따라 새 지도 생성
            history.push({
                path: '/detail',
                state: {lat: circles[0].getPosition().getLat(), lng: circles[0].getPosition().getLng(), id: circles[0].getTitle()} 
            });
        });

        kakao.maps.event.addListener(circles[1], 'click', function () {

            history.push({
                path: '/detail',
                state: {lat: circles[1].getPosition().getLat(), lng: circles[1].getPosition().getLng(), id: circles[1].getTitle()} 
            });
            
        });

        kakao.maps.event.addListener(circles[2], 'click', function () {
            history.push({
                path: '/detail',
                state: {lat: circles[2].getPosition().getLat(), lng: circles[2].getPosition().getLng(), id: circles[2].getTitle()} 
            });
        });

        kakao.maps.event.addListener(circles[3], 'click', function () {
            history.push({
                path: '/detail',
                state: {lat: circles[3].getPosition().getLat(), lng: circles[3].getPosition().getLng(), id: circles[3].getTitle()} 
            });
        });

        kakao.maps.event.addListener(circles[4], 'click', function () {
            history.push({
                path: '/detail',
                state: {lat: circles[4].getPosition().getLat(), lng: circles[4].getPosition().getLng(), id: circles[4].getTitle()} 
            });
        });
    }
}

export default Masl;