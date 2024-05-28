import React from 'react';
import { Routes, Route, BrowserRouter } from 'react-router-dom';
import AddTestCaseForm from './addTest/addTest.js';
import ButtonGroup from './main/button.js';
import HeaderBar from './header/headerBar.js'
import List from './testList/testList.js'
import Result from './result/result.js';

const RouterComponent = () => {
  return (
    <BrowserRouter>
      <HeaderBar />
      <Routes>
        <Route path="/" element={<ButtonGroup />} />
        <Route path="/add" element={<AddTestCaseForm />} />
        <Route path="/list" element={<List />} />
        <Route path="/result/:id" element={<Result />} />
      </Routes>
    </BrowserRouter>
  );
}

export default RouterComponent;
