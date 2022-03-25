import React from 'react'
import { Login } from './components/Login';
import { Register } from './components/Register';

export const App: React.FC = () => {
  return (<>
    <Login />
    <Register />
  </>);
}