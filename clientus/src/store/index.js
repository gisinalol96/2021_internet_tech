import Vue from 'vue';
import Vuex from 'vuex';

import api from '@/api/api';
import { cloneObject } from '@/helpers';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    customers: [],
  },

  getters: {
    getCustomerByID: state => id => state.customers.find(customer => customer.customerID === id),

    getCustomers: state => state.customers,
  },

  mutations: {
    setCustomers(state, customers) {
      state.customers = customers;
    },

    addCustomer(state, customer) {
      state.customers.push(customer);
    },

    addBillboard(state, { billboard, customerID }) {
      const currentCustomer = state.customers.find(customer => customer.customerID === customerID);
      currentCustomer.billboards.push(billboard);
    },

    updateBillboard(state, { customerID, newBillboard }) {
      const currentCustomer = state.customers.find(customer => customer.customerID === customerID);
      const currentBillboard = currentCustomer.billboards.findIndex(billboard => billboard.billboardID === newBillboard.billboardID);

      currentCustomer.billboards[currentBillboard] = { ...newBillboard };
    },

    changeBillboardCustomer(state, { currentCustomerID, newCustomerID, updatedBillboard }) {
      const currentCustomer = state.customers.find(customer => customer.customerID === currentCustomerID);
      const deletedBillboard = currentCustomer.billboards.findIndex(billboard => billboard.billboardID === updatedBillboard.billboardID);

      // remove item from array: (itemIndex, numberOfRemovableItems)
      currentCustomer.billboards.splice(deletedBillboard, 1);

      const newCustomer = state.customers.find(customer => customer.customerID === newCustomerID);
      newCustomer.billboards.push(updatedBillboard);
    },

    deleteBillboard(state, { customerID, billboardID }) {
      const currentCustomer = state.customers.find(customer => customer.customerID === customerID);
      const deletedBillboard = currentCustomer.billboards.findIndex(billboard => billboard.billboardID === billboardID);

      currentCustomer.billboards.splice(deletedBillboard, 1);
    },
  },

  actions: {
    async getCustomers({ commit }) {
      try {
        const customers = await api.getCustomers();
        commit('setCustomers', customers);
      } catch (e) {
        console.error('Error:', e);
      }
    },

    async addCustomer({ commit }, customer) {
      await api.addCustomer(customer);

      commit('addCustomer', customer);
    },

    async addBillboard({ commit }, { customerID, billboard }) {
      await api.addBillboard(customerID, billboard);

      commit('addBillboard', {
        billboard: cloneObject(billboard),
        customerID,
      });
    },

    async updateBillboard({ commit }, { customerID, newBillboard }) {
      await api.updateBillboard(customerID, newBillboard.billboardID, newBillboard);

      commit('updateBillboard', {
        customerID,
        newBillboard: cloneObject(newBillboard),
      });
    },

    async changeBillboardCustomer({ commit }, { currentCustomerID, newCustomerID, updatedBillboard }) {
      await api.changeBillboardCustomer(currentCustomerID, newCustomerID, updatedBillboard.billboardID);

      commit('changeBillboardCustomer', {
        currentCustomerID,
        newCustomerID,
        updatedBillboard,
      });
    },

    async deleteBillboard({ commit }, { customerID, billboardID }) {
      await api.deleteBillboard(customerID, billboardID);

      commit('deleteBillboard', {
        customerID,
        billboardID,
      });
    },
  },
});
