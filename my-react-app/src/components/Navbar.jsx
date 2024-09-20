import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBell, faWandMagicSparkles } from '@fortawesome/free-solid-svg-icons';
import { BrowserRouter as Router, Route, Routes, Link, useLocation } from 'react-router-dom';
import { faUser } from '@fortawesome/free-solid-svg-icons'; // Import the icon you want

const Navbar = () => {
  // Get the current path
  const location = useLocation();

  return (
    <>
      <section className='font-suse text-md'>
        <div className='flex flex-row justify-between items-center p-2'>
          <div className='font-chakra text-3xl bg-black text-white p-1 rounded-lg'>
            Eshcrop
          </div>
          <div className="flex flex-row gap-4">
            <div className="relative">
              {/* Apply underline if current path is '/' */}
              <span className={`cursor-pointer ${location.pathname === '/' ? 'after:w-full' : 'hover:after:w-full'} hover:after:animate-underline-expand after:absolute after:left-1/2 after:bottom-0 after:h-[2px] after:w-0 after:bg-black after:transition-all after:duration-300 after:ease-out after:transform after:-translate-x-1/2`}>
                <Link to="/">Dashboard</Link>
              </span>
            </div>
            <div className="relative">
              {/* Apply underline if current path is '/my_portfolio' */}
              <span className={`cursor-pointer ${location.pathname === '/my_portfolio' ? 'after:w-full' : 'hover:after:w-full'} hover:after:animate-underline-expand after:absolute after:left-1/2 after:bottom-0 after:h-[2px] after:w-0 after:bg-black after:transition-all after:duration-300 after:ease-out after:transform after:-translate-x-1/2`}>
                <Link to="/my_portfolio">My portfolio</Link>
              </span>
            </div>
          </div>
          <div className='flex flex-row gap-4 items-center'>
            <div>Saved</div>
            <div>Lists</div>
            <button className="relative overflow-hidden flex flex-row justify-center items-center gap-1 text-white bg-slate-700 p-2 rounded-lg group">
              <span className="relative z-10 flex items-center">
                <div>Generate</div>
                <FontAwesomeIcon icon={faWandMagicSparkles} className="ml-2" />
              </span>
              <span className="absolute inset-0 bg-black origin-center transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500"></span>
            </button>
          </div>
          <div className='flex flex-row gap-2 items-center justify-center mr-3'>

            <FontAwesomeIcon icon={faBell} className="text-black-500 hover:cursor-pointer" />
            <div>|</div>
            <div className='flex flex-row justify-center items-center gap-1 hover:cursor-pointer'>
            <div className="flex items-center justify-center">
                <div className="bg-gray-200 p-1 rounded-full flex items-center justify-center">
                    <FontAwesomeIcon icon={faUser} className="text-gray-700 " />
                </div>
            </div>
            <div>User</div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default Navbar;
