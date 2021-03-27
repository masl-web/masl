/* code by 성민 */
import React from 'react';

import { useEffect, useState } from 'react';

import { Button, Modal } from 'react-bootstrap';

import Postcode from "./Postcode";
import './modal.css'

function ModalAddress({ open, closeModal, header, address, setAddress }) {
    useEffect(() => {
        if(!!address) return
            console.log("OK 선택");
            console.log(address);
            closeModal();
      }, [address])
    // 열기, 닫기, 모달 헤더 텍스트를 부모로부터 받아옴
    return (
        // 모달이 열릴때 openModal 클래스가 생성된다.
        <div className={ open ? 'openModal modal' : 'modal' }>
            { open ? (  
                <section>
                    <header>
                        {header}
                        <button className="close" onClick={closeModal}> &times; </button>
                    </header>
                    <main>
                        <Postcode address={address} setAddress={()=>{setAddress();}}/>
                    </main>
                    <footer>
                        <button className="close" onClick={closeModal}> close </button>
                    </footer>
                </section>
            ) : null }
        </div>
    )
  }

export default ModalAddress;