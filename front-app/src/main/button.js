import React from 'react';
import './button.css';
import { Link } from 'react-router-dom';

const ButtonGroup = () => {
  console.log("ButtonGroup rendered");
  return (
    <div className="button-group">
      <Link to='/add'><button className="btn">테스트 <br></br> 추가하기</button></Link>
      <Link to='/list'><button className="btn">테스트 <br></br> 목록보기</button></Link>
    </div>
  );
};

export default ButtonGroup;
