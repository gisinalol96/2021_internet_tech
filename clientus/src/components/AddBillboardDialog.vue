<template>
  <ElDialog
    title="Добавить биллборд"
    :visible.sync="showDialog"
    width="500px"
    destroy-on-close
    @open="loadData"
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

      <ElButton
        type="primary"
        :disabled="isDisabled"
        @click="addBillboard()"
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

    customerID: {
      default: '',
    },
  },

  data() {
    return {
      showDialog: false,
      customer: {},
      billboard: {
        billboardID: '',
        info: '',
        address: '',
      },
    };
  },

  computed: {
    isDisabled() {
      return !this.billboard.info;
    },
  },

  methods: {
    loadData() {
      this.customer = this.$store.getters.getCustomerByID(this.customerID);
    },

    async addBillboard() {
      this.billboard.billboardID = this.generateBillboardID();
      await this.$store.dispatch('addBillboard', {
        customerID: this.customerID,
        billboard: cloneObject(this.billboard),
      });

      this.cancel();
    },

    cancel() {
      this.showDialog = false;
      this.clearBillboardInfo();
    },

    clearBillboardInfo() {
      this.billboard.billboardID = '';
      this.billboard.info = '';
      this.billboard.address = '';
    },

    generateBillboardID() {
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
