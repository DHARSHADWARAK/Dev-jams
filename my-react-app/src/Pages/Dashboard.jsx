import React, { useState } from 'react';


const Dashboard = () => {
  const [selectedOption, setSelectedOption] = useState('Last 30 Days'); // Default value

  const options = [
    'Last 30 Days',
    'Last One Day',
    'Last Week',
    'Last Year',
    'Max'
  ];

  const handleSelect = (option) => {
    setSelectedOption(option);
    // You can add additional logic here to handle the selection
    console.log(`Selected: ${option}`);
  };
  return (
    <>
    <section className='font-suse text-md p-2 text-lg'>
      <div className='text-3xl font-black	text-gray-400 py-4'>
        DASHBOARD
      </div>
      <div className='flex flex-row '>
        <div className='flex flex-col justify-start items-start bg-gray-200 w-1/2'>
            <span className='font-semibold	'>Evaluation</span>
            <span className='text-sm text-gray-500'>Total assets</span>
            <div className='flex flex-row justify-between items-center w-full '>
              <div className='flex flex-row justify-center items-baseline gap-2'>
                <span className='text-lg font-bold'>
                $69,696.69
                </span >
                <div className='text-xs p-[2px] bg-green-400 rounded-sm'>
                  1.9%
                </div>
                <div className='text-xs p-[2px] bg-green-400 rounded-sm'>

                  $747.27
                </div>
              </div>
              <div>
              <div className="relative inline-block text-left">
      <div>
        <button
          type="button"
          className="inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          id="menu-button"
          aria-expanded="true"
          aria-haspopup="true"
        >
          {selectedOption}
          <svg
            className="-mr-1 ml-2 h-5 w-5"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            aria-hidden="true"
          >
            <path
              fillRule="evenodd"
              d="M5.23 7.21a.75.75 0 011.06-.02L10 10.36l3.71-3.17a.75.75 0 011.08 1.04l-4.25 3.63a.75.75 0 01-1.08 0L5.23 8.25a.75.75 0 01-.02-1.06z"
              clipRule="evenodd"
            />
          </svg>
        </button>
      </div>

      {/* Dropdown panel */}
      <div
        className="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
        role="menu"
        aria-orientation="vertical"
        aria-labelledby="menu-button"
        tabIndex="-1"
      >
        <div className="py-1  " role="none">
          {options.map((option) => (
            <button
              key={option}
              onClick={() => handleSelect(option)}
              className="text-gray-700 block px-4 py-2 text-sm w-full text-left hover:bg-gray-100"
              role="menuitem"
              tabIndex="-1"
            >
              {option}
            </button>
          ))}
        </div>
      </div>
    </div>
              </div>
            </div>
        </div>
        <div>

        </div>
      </div>
    </section>
    </>
  )
}

export default Dashboard