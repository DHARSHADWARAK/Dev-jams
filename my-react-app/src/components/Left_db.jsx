import React from 'react';
import '../App.css'; // Import the CSS file for flip styles

const CardList = () => {
    const data = [
        {
          symbol: 'BTC',
          name: 'Bitcoin',
          shortform: 'BTC',
          value: 0.264,
          percentage: 19.62,
        },
        {
          symbol: 'ETH',
          name: 'Ethereum',
          shortform: 'ETH',
          value: 3.05,
          percentage: 12.28,
        },
        {
          symbol: 'ADA',
          name: 'Cardano',
          shortform: 'ADA',
          value: 21390,
          percentage: 16.1,
        },
        {
          symbol: 'ALGO',
          name: 'Algorand',
          shortform: 'ALGO',
          value: 44351,
          percentage: 11.66,
        },
        {
          symbol: 'DOT',
          name: 'Polkadot',
          shortform: 'DOT',
          value: 1096,
          percentage: 11.24,
        },
        {
          symbol: 'POWR',
          name: 'Power Ledger',
          shortform: 'POWR',
          value: 21017,
          percentage: 10.97,
        },
        {
          symbol: 'SLR',
          name: 'Solar Coin',
          shortform: 'SLR',
          value: 104080,
          percentage: 9.61,
        },
        {
          symbol: 'LINK',
          name: 'Chainlink',
          shortform: 'LINK',
          value: 304,
          percentage: 8.52,
        },
      ];

  return (
    <div className='md:w-1/2'>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4   gap-[1rem]">
          {data.map((service, index) => (
            <div key={index} className='flip-box w-full'>
              <div className="flip-box-inner">
                <div className='flip-box-front flex bg-gray-100 p-2 rounded-lg shadow-lg text-gray-800 items-center justify-center'>
                  <div className='flex flex-col justify-center items-center'>
                  <div className='flex text-xl font-semibold '>
                    {service.symbol}
                    </div>
                  <img src="src\assets\—Pngtree—vector star icon_4231909.png" className='w-[40%]' alt="" />{/*Use symbol related to the section*/}
                  </div>
                </div>
                <div className='flex flex-col justify-between flip-box-back  bg-gray-100 p-2 rounded-lg shadow-lg text-gray-800'>
                    <div>
                        <div className="text-xl font-semibold mb-1">{service.name}</div>
                        <div className="text-base font-semibold ">{service.shortform}</div>
                    </div>
                    <div>
                        <p className="leading-relaxed">
                            {service.value}
                        </p>
                        <p className="leading-relaxed">
                            {service.percentage}%
                        </p>
                    </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="flex flex-col">
      {data.map((item, index) => (
        <div
          key={index}
          className="flex items-center p-4 border-b hover:bg-gray-100"
        >
          {/* Symbol/Icon */}
          <div className="w-12 h-12 bg-gray-200 flex items-center justify-center rounded-full">
            {/* Replace the text with an actual icon if available */}
            <span className="text-lg font-bold">{item.symbol}</span>
          </div>

          {/* Name and Shortform */}
          <div className="flex flex-col ml-4">
            <span className="font-semibold text-gray-800">{item.name}</span>
            <span className="text-sm text-gray-500">{item.shortform}</span>
          </div>

          {/* Value and Percentage */}
          <div className="flex flex-col ml-auto text-right">
            <span className="font-semibold text-gray-800">
              {item.value.toLocaleString()}
            </span>
            <span
              className={`text-sm ${
                item.percentage >= 0 ? 'text-green-500' : 'text-red-500'
              }`}
            >
              {item.percentage}%
            </span>
          </div>
        </div>
      ))}
    </div>
    </div>
  );
};

export default CardList;
