import React, { useState } from 'react';

const Duration_Dropdown = () => {
    const [selectedOption, setSelectedOption] = useState('Last 30 Days'); // Default value
  const [isOpen, setIsOpen] = useState(false);

  const options = [
    'Last Day',
    'Last Week',
    'Last Month',
    'Last Year',
    'Max',
  ];

  const handleSelect = (option) => {
    setSelectedOption(option);
    setIsOpen(false); // Close the dropdown
    console.log(`Selected: ${option}`);
  };
  return (
    <>
         <div>
              {/* Dropdown code remains the same */}
              <div className="relative inline-block text-left">
                <div>
                  <button
                    type="button"
                    onClick={() => setIsOpen(!isOpen)}
                    className="inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-2 py-1 bg-gray-29 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none"
                    id="menu-button"
                    aria-expanded={isOpen}
                    aria-haspopup="true"
                  >
                    {selectedOption}
                    {/* SVG Icon */}
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
                {isOpen && (
                  <div
                    className="origin-top-right absolute right-0 mt-2 w-auto rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
                    role="menu"
                    aria-orientation="vertical"
                    aria-labelledby="menu-button"
                  >
                    <div className="py-1" role="none">
                      {options.map((option) => (
                        <button
                          key={option}
                          onClick={() => handleSelect(option)}
                          className="text-gray-700 block px-2 py-1 text-sm w-auto text-left hover:bg-gray-100"
                          role="menuitem"
                        >
                          {option}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
              {/* End of dropdown code */}
            </div>
    </>
  )
}

export default Duration_Dropdown