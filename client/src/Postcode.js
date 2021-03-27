/* code by 성민 */
import React from 'react';
import DaumPostcode from 'react-daum-postcode';

import { useEffect, useState } from 'react';

function Postcode({ setAddress }){
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
      setAddress(fullAddress);
    }

    return (
      <DaumPostcode
        onComplete={handleComplete}
      />
    );
  }
  
  export default Postcode;