<template>
  <ElDialog
    title="Добавить заказчика"
    :visible.sync="showDialog"
    width="500px"
    destroy-on-close
    @close="$emit('close')"
  >
    <ElForm
      label-position="left"
      label-width="120px"
    >
      <ElFormItem
        label="Название компании"
        label-width="150px"
      >
        <ElInput v-model="customer.customerName" />
      </ElFormItem>

      <ElButton
        type="primary"
        :disabled="isDisabled"
        @click="addCustomer()"
      >
        Добавить
      </ElButton>

      <ElButton
        @click="cancel()"
      >
        Отмена
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
  },

  data() {
    return {
      showDialog: false,
      customer: {
        customerName: '',
        customerID: '',
      },
    };
  },

  computed: {
    isDisabled() {
      return !this.customer.customerName;
    },
  },

  methods: {
    addCustomer() {
      this.customer.customerID = this.generateCustomerID();

      this.$store.dispatch('addCustomer', cloneObject(this.customer));

      this.cancel();
    },

    cancel() {
      this.showDialog = false;
      this.clearCustomerInfo();
    },

    clearCustomerInfo() {
      this.customer.customerName = '';
      this.customer.customerID = '';
    },

    generateCustomerID() {
      const id = +(new Date()).getTime();

      return id;
    },
  },

  watch: {
    dialogVisible() {
      this.showDialog = this.dialogVisible;
    },
  },
};
</script>
