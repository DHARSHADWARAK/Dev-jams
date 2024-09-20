import { useState } from 'react'
import Dashboard from './Pages/Dashboard'
import Navbar from './components/Navbar'
import Signup from './Pages/Signup'
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import My_portfolio from './Pages/My_portfolio';

function App() {
  return (
    <>
    <Router>
      <Navbar/>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/my_portfolio" element={<My_portfolio/>} />
      </Routes>
    </Router>
    </>
  )
}

export default App
