import React, { useState } from "react";

function Checkbox({ id, name, image }) {
    const [isChecked, setIsChecked] = useState(false);

    function checkHandler() {
        setIsChecked(!isChecked)
    } 

    return (
        <>
            <input type="checkbox" checked={isChecked} name={name} onChange={checkHandler} />
            {name}
        </>
    );
  }
  

export default function CheckboxList({ id, data }) {    
    
    const [checkedCafes, setCheckedCafes] = useState([]);

    function listChangeHandler(e) {
      console.log(e.target.name, e.target.checked);

      if (e.target.checked) {
        setCheckedCafes([...checkedCafes, e.target.name]);
      } else {
        const newList = [...checkedCafes].filter(cafe => cafe !== e.target.name);
        setCheckedCafes(newList);
      }

      // console.log(checkedCafes);
    }

    return (
      <>
        <div id={id} onChange={listChangeHandler}>
            {data.map((cafe, index) => (
                <Checkbox key={index} name={cafe} />
            ))}
        </div>
      </>
    );
}