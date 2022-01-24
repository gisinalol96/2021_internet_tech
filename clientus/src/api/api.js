const baseUrl = ' http://127.0.0.1:5000';

export default {
  getCustomers: async () => {
    const res = await fetch(`${baseUrl}/customers`);
    const data = await res.json();
    return data;
  },

  addCustomer: async customer => {
    await fetch(`${baseUrl}/customers`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(customer),
    });
  },

  addBillboard: async (customerID, billboard) => {
    await fetch(`${baseUrl}/customers/${customerID}/billboards`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(billboard),
    });
  },

  updateBillboard: async (customerID, billboardID, billboard) => {
    await fetch(`${baseUrl}/customers/${customerID}/billboards/${billboardID}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        info: billboard.info,
        address: billboard.address,
      }),
    });
  },

  deleteBillboard: async (customerID, billboardID) => {
    await fetch(`${baseUrl}/customers/${customerID}/billboards/${billboardID}`, {
      method: 'DELETE',
    });
  },

  changeBillboardCustomer: async (oldCustomerID, newCustomerID, billboardID) => {
    const idData = {
      to_customerID: newCustomerID,
      billboardID,
    };

    await fetch(`${baseUrl}/customers/${oldCustomerID}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(idData),
    });
  },
};
