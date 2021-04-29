/* code by 성민 */
import React, { useEffect, useState } from 'react';
import DaumPostcode from 'react-daum-postcode';
import { useDispatch } from 'react-redux';
import { setAddress, setLocation } from './actions';

const { kakao } = window;

function Postcode(){

    const geocoder = new kakao.maps.services.Geocoder(); // 주소-좌표 변환 객체를 생성합니다

    const dispatch = useDispatch();
    
    const handleComplete = (data) => {
      let fullAddress = data.address;
      let extraAddress = ''; 

      if (data.addressType === 'R') {
        if (data.bname !== '') {
          extraAddress += data.bname;
        }
        if (data.buildingName !== '') {
          extraAddress += (extraAddress !== '' ? `, ${data.buildingName}` : data.buildingName);
        }
        fullAddress += (extraAddress !== '' ? ` (${extraAddress})` : '');
      }
      
      // 주소로 좌표를 검색합니다
      geocoder.addressSearch(fullAddress, function(result, status) {
        // 정상적으로 검색이 완료됐으면 
         if (status === kakao.maps.services.Status.OK) {
            console.log(result[0].y);
            console.log(result[0].x);
            dispatch(setLocation([result[0].y, result[0].x]))
        } else {
          console.log('주소 좌표 검색 실패')
        }
    })

      dispatch(setAddress(fullAddress));
    }

    return (
      <DaumPostcode
        onComplete={handleComplete}
      />
    );
  }
  
  export default Postcode;