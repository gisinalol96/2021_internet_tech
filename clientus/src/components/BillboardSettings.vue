<template>
  <ElDialog
    title="Детали биллборда"
    :visible.sync="showDialog"
    width="500px"
    destroy-on-close
    @open="getData"
    @close="$emit('close')"
  >
    <ElForm
      label-position="left"
      label-width="150px"
    >
      <ElFormItem label="Текст">
        <ElInput v-model="billboard.info" />
      </ElFormItem>

      <ElFormItem label="Адрес">
        <ElInput v-model="billboard.address" />
      </ElFormItem>

      <ElFormItem label="Сменить компанию">
        <ElSelect
          v-model="selectedCustomerID"
          placeholder="Выберите компанию"
        >
          <el-option
            v-for="customer in filteredCustomers"
            :key="customer.customerID"
            :label="customer.customerName"
            :value="customer.customerID">
          </el-option>
        </ElSelect>
      </ElFormItem>

      <ElButton
        type="primary"
        @click="apply()"
      >
        Изменить
      </ElButton>

      <ElButton
        @click="cancel()"
      >
        Отмена
      </ElButton>

      <ElButton
        @click="remove()"
      >
        Удалить биллборд
      </ElButton>
    </ElForm>
  </ElDialog>
</template>

<script>
import { cloneObject } from '@/helpers';

export default {
  props: {
    dialogVisible: {
      default: false,
    },

    customerID: {
      default: '',
    },

    billboardID: {
      default: '',
    },
  },

  data() {
    return {
      showDialog: false,
      customer: {},
      billboard: {},
      selectedCustomerID: {},
    };
  },

  computed: {
    filteredCustomers() {
      return this.$store.getters.getCustomers;
    },
  },

  methods: {
    getData() {
      this.customer = this.$store.getters.getCustomerByID(this.customerID);
      this.selectedCustomerID = this.customer.customerID;
      const billboardCopy = this.customer.billboards.find(billboard => billboard.billboardID === this.billboardID);

      this.billboard = cloneObject(billboardCopy);
    },

    async apply() {
      if (this.customerID === this.selectedCustomerID) {
        await this.$store.dispatch('updateBillboard', {
          customerID: this.selectedCustomerID,
          newBillboard: cloneObject(this.billboard),
        });
      } else {
        await this.$store.dispatch('changeBillboardCustomer', {
          currentCustomerID: this.customerID,
          newCustomerID: this.selectedCustomerID,
          updatedBillboard: cloneObject(this.billboard),
        });
      }
      this.cancel();
    },

    cancel() {
      this.showDialog = false;
    },

    async remove() {
      await this.$store.dispatch('deleteBillboard', {
        customerID: this.customerID,
        billboardID: this.billboard.billboardID,
      });
      this.cancel();
    },
  },

  watch: {
    dialogVisible() {
      this.showDialog = this.dialogVisible;
    },
  },
};
</script>
