import React from 'react';
import Duration_Dropdown from '../components/Duration_Dropdown';

const Right_db = () => {
  // Constants for general values
  const EVALUATION_LABEL = 'Evaluation';
  const TOTAL_ASSETS_LABEL = 'Total assets';
  const TOTAL_ASSETS_VALUE = '$69,696';
  const TOTAL_ASSETS_DECIMAL = '.69';
  const PERCENTAGE_CHANGE = 1.9; // Replace with your actual data
  const DOLLAR_CHANGE = '$747.27';
  const PERFORMANCE_MESSAGE = 'Strong performance 💪';
  const GRAPH_IMAGE_SRC = '/src/assets/graphs dummy.webp';

  // Constants for portfolio score
  const PORTFOLIO_NUMERIC_SCORE = 65; // Replace with your actual score

  // Constants for data array
  const TOTAL_PROFIT_HEADING = 'Total profit';
  const TOTAL_PROFIT_VALUE = '+$6,801.19';
  const TOTAL_PROFIT_FEEDBACK = '+15.81%';

  const AVG_MONTHLY_GROWTH_HEADING = 'Avg. Monthly Growth';
  const AVG_MONTHLY_GROWTH_VALUE = '~1.34%';
  const AVG_MONTHLY_GROWTH_FEEDBACK = '~$523';

  const BEST_PROFIT_TOKEN_HEADING = 'Best-Profit Token';
  const BEST_PROFIT_TOKEN_VALUE = 'Cardano';
  const BEST_PROFIT_TOKEN_FEEDBACK = 'ADA';

  const AIRA_HEADING = 'AIRA';
  const AIRA_VALUE = '74%';
  const AIRA_FEEDBACK = 'Rebalance accuracy';

  const PRI_HEADING = 'PRI';
  const PRI_VALUE = '0.45';
  const PRI_FEEDBACK = 'Resilience Index: Risky';

  // Function to calculate the grade
  const getGrade = (score) => {
    if (score >= 90) return 'A';
    else if (score >= 80) return 'B';
    else if (score >= 70) return 'C';
    else if (score >= 60) return 'D';
    else return 'F';
  };

  const getFeedback = (score) => {
    if (score >= 90) return 'Excellent';
    else if (score >= 80) return 'Very good';
    else if (score >= 70) return 'Good';
    else if (score >= 60) return 'Nice';
    else return 'Could be better';
  };

  const portfolioGrade = getGrade(PORTFOLIO_NUMERIC_SCORE); // Calculate the grade
  const portfolioFeedback = getFeedback(PORTFOLIO_NUMERIC_SCORE);

  // Data array for mapping
  const data = [
    {
      heading: TOTAL_PROFIT_HEADING,
      value: TOTAL_PROFIT_VALUE,
      feedback: TOTAL_PROFIT_FEEDBACK,
    },
    {
      heading: AVG_MONTHLY_GROWTH_HEADING,
      value: AVG_MONTHLY_GROWTH_VALUE,
      feedback: AVG_MONTHLY_GROWTH_FEEDBACK,
    },
    {
      heading: BEST_PROFIT_TOKEN_HEADING,
      value: BEST_PROFIT_TOKEN_VALUE,
      feedback: BEST_PROFIT_TOKEN_FEEDBACK,
    },
    {
      heading: 'Portfolio Score',
      value: `${PORTFOLIO_NUMERIC_SCORE}/100`,
      grade: portfolioGrade,
      feedback: portfolioFeedback,
    },
    {
      heading: AIRA_HEADING,
      value: AIRA_VALUE,
      feedback: AIRA_FEEDBACK,
    },
    {
      heading: PRI_HEADING,
      value: PRI_VALUE,
      feedback: PRI_FEEDBACK,
    },
  ];

  return (
    <>
      <div className="flex flex-col justify-start items-start bg-white gap-2 md:w-1/2">
        {/* Existing content */}
        <span className="font-semibold">{EVALUATION_LABEL}</span>
        <span className="text-sm text-gray-500">{TOTAL_ASSETS_LABEL}</span>
        <div className="flex flex-row justify-between items-center w-full">
          <div className="flex flex-row justify-center items-baseline gap-1">
            <div className="flex flex-row justify-center items-baseline text-lg font-bold">
              <div>{TOTAL_ASSETS_VALUE}</div>
              <div className="text-sm">{TOTAL_ASSETS_DECIMAL}</div>
            </div>
            <div className="flex flex-row items-center gap-1">
              <div
                className={`flex items-center text-xs p-[2px] ${
                  PERCENTAGE_CHANGE >= 0 ? 'bg-green-400' : 'bg-red-400'
                } rounded-sm`}
              >
                {PERCENTAGE_CHANGE >= 0 ? (
                  <svg
                    className="w-3 h-3 mr-1"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    {/* Upward Triangle */}
                    <path d="M10 5l5 10H5l5-10z" />
                  </svg>
                ) : (
                  <svg
                    className="w-3 h-3 mr-1"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    {/* Downward Triangle */}
                    <path d="M10 15l5-10H5l5 10z" />
                  </svg>
                )}
                {Math.abs(PERCENTAGE_CHANGE)}%
              </div>
              <div className="text-xs p-[2px] bg-green-400 rounded-sm">
                {DOLLAR_CHANGE}
              </div>
            </div>
          </div>
          <Duration_Dropdown />
        </div>
        <div className="text-xs font-semibold text-gray-600 p-1 border border-gray-400 rounded-lg">
          {PERFORMANCE_MESSAGE}
        </div>
        <img src={GRAPH_IMAGE_SRC} alt="Graph" />
        {/* Updated Flex Box with Constant Height */}
        <div>
          <div className="flex flex-wrap">
            {data.map((item, index) => (
              <div
                key={index}
                className="w-full sm:w-1/2 lg:w-1/3 p-2"
              >
                <div className="bg-white p-4 shadow rounded transform transition duration-500 hover:cursor-pointer hover:scale-105 hover:bg-black hover:text-white group h-40 flex flex-col justify-between">
                  <h3 className="text-gray-600 text-sm font-semibold group-hover:text-white">
                    {item.heading}
                  </h3>
                  {item.grade ? (
                    // Display both grade and score for Portfolio Score
                    <div className="flex flex-row gap-2 items-center">
                      <p
                        className={`font-bold text-3xl md:text-2xl text-white w-12 h-12 md:w-8 md:h-8 flex items-center justify-center rounded-full ${
                          item.grade === 'A'
                            ? 'bg-green-600'
                            : item.grade === 'B'
                            ? 'bg-green-500'
                            : item.grade === 'C'
                            ? 'bg-yellow-500'
                            : item.grade === 'D'
                            ? 'bg-orange-500'
                            : 'bg-red-600'
                        }`}
                      >
                        {item.grade}
                      </p>
                      <p className="font-bold group-hover:text-white text-3xl md:text-2xl">
                        {item.value}
                      </p>
                    </div>
                  ) : (
                    // Display only the value for other items
                    <p className="font-bold group-hover:text-white text-3xl md:text-2xl">
                      {item.value}
                    </p>
                  )}
                  <p className="text-gray-500 text-sm group-hover:text-gray-300">
                    {item.feedback}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      {/* Other content */}
    </>
  );
};

export default Right_db;
