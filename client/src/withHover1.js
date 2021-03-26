import React, { useState } from "react";
import './withHover1.css';

function Checkbox_cafe({ id, name, image }) {
    const [isChecked, setIsChecked] = useState(false);

    function changeHandler() {
        setIsChecked(!isChecked)
    } 

    return (
      <div className="cafe-check">
        <input type="checkbox" id={id} name={name} checked={isChecked} onChange={changeHandler}/>
        <label htmlFor={id}>
          <div className="chk_img">
            <img src={image} alt={name} />
          </div>
        </label>
      </div>
    );
  }
  

function CafeList() {

    const cafes = [
        {
          id: 1,
          name: "starbucks",
          image: "./images/starbucks_logo.png",
        },
        {
          id: 2,
          name: "paulbassett",
          image: "./images/paulbassett_logo.png",
        },
        {
          id: 3,
          name: "angelinus",
          image: "./images/angelinus_logo.png",
        },
        {
          id: 4,
          name: "hollys",
          image: "./images/hollys_logo.png",
        },
        {
          id: 5,
          name: "coffeebin",
          image: "./images/coffeebin_logo.png",
        },
        {
          id: 6,
          name: "gongcha",
          image: "./images/gongcha_logo.png",
        },
      ];      
    
    const [checkedCafes, setCheckedCafes] = useState([]);

    function listChangeHandler(e) {
      console.log(e.target.name, e.target.checked);

      if (e.target.checked) {
        setCheckedCafes([...checkedCafes, e.target.name]);
      } else {
        const newList = [...checkedCafes].filter(cafe => cafe !== e.target.name);
        setCheckedCafes(newList);
      }

      console.log(checkedCafes);
    }

    return (
      <>
        <div id="Cafe" onChange={listChangeHandler}>
            {cafes.map((cafe) => (
                <Checkbox_cafe key={cafe.id} id={cafe.id} name={cafe.name} image={cafe.image} />
            ))}
        </div>
      </>
    );
}

export default function _UserInfo() {

    return (
        <>
            <form>
                <p>카페</p>
                <CafeList/>
            </form>
        </>
        
    )
}