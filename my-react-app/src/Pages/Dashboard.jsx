import React from 'react';
import Right_db from '../components/Right_db';
import Left_db from '../components/Left_db';

const Dashboard = () => {
  const DASHBOARD_TITLE = 'DASHBOARD';


  return (
    <section className="font-suse text-md p-2 text-lg">
      <div className="text-3xl font-black text-gray-400 py-4">{DASHBOARD_TITLE}</div>
    <div className="flex flex-col md:flex-row gap-2 ">
      <Right_db/>
      <Left_db/>
    </div>
    </section>
  );
};

export default Dashboard;
