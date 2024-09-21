import React, { useState } from 'react';
import '../components/Form.css'
const User = () => {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    riskApetite: 'medium',
    phone: '',
    email: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form Data:', formData);
  };

  const Title = "FORM";

  return (
    <section className='font-suse text-md p-4 md:p-6  rounded-lg shadow-md'>
      <div className="text-3xl font-black text-gray-400 pb-2">{Title}</div>
      <form onSubmit={handleSubmit} className="space-y-6 pl-0 pr-0 md:pl-[25vw] md:pr-[25vw]">
        <div>
          <label htmlFor="name" className="block text-lg text-gray-700">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-gray-500 bg-gray-50"
            required
          />
        </div>

        <div>
          <label htmlFor="age" className="block text-lg text-gray-700">Age:</label>
          <input
            type="number"
            id="age"
            name="age"
            value={formData.age}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-gray-500 bg-gray-50"
            required
          />
        </div>

        <div>
          <label className="block text-lg text-gray-700">Risk Appetite:</label>
          <div className="flex space-x-4">
            <label className="inline-flex items-center text-gray-600">
              <input
                type="radio"
                name="riskApetite"
                value="high"
                checked={formData.riskApetite === 'high'}
                onChange={handleChange}
                className="custom-radio"
              />
              <span className="ml-2">High</span>
            </label>
            <label className="inline-flex items-center text-gray-600">
              <input
                type="radio"
                name="riskApetite"
                value="medium"
                checked={formData.riskApetite === 'medium'}
                onChange={handleChange}
                className="custom-radio"
              />
              <span className="ml-2">Medium</span>
            </label>
            <label className="inline-flex items-center text-gray-600">
              <input
                type="radio"
                name="riskApetite"
                value="low"
                checked={formData.riskApetite === 'low'}
                onChange={handleChange}
                className="custom-radio"
              />
              <span className="ml-2">Low</span>
            </label>
          </div>
        </div>

        <div>
          <label htmlFor="phone" className="block text-lg text-gray-700">Phone Number:</label>
          <input
            type="tel"
            id="phone"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-gray-500 bg-gray-50"
            required
          />
        </div>

        <div>
          <label htmlFor="email" className="block text-lg text-gray-700">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-gray-500 bg-gray-50"
            required
          />
        </div>

        <button type="submit" className="w-full py-3 bg-black text-white rounded">
  <span>Submit</span>
</button>

      </form>
    </section>
  );
};

export default User;
