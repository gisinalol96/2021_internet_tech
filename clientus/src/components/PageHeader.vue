<template>
  <div class="header">
    <div class="title">Личный кабинет менеджера рекламного агенства</div>
    <div class="btn-wrapper">
      <el-button
        class="add-customer-btn"
        @click="customerDialogVisible = true"
      >
        Добавить заказчика <i class="el-icon-plus el-icon-right"></i>
      </el-button>
    </div>

    <AddCustomerDialog
      :dialogVisible.sync="customerDialogVisible"
      @close="customerDialogVisible = false"
    />
  </div>
</template>

<script>
import AddCustomerDialog from './AddCustomerDialog.vue';

export default {
  components: {
    AddCustomerDialog,
  },

  data() {
    return {
      customerDialogVisible: false,
    };
  },
};
</script>

<style lang="scss" scoped>
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    height: 60px;
    top: 0;
    background: #f2952e;
    padding-left: 50px;
    padding-right: 50px;
    box-shadow: 0px 4px 8px 0px rgba(34, 60, 80, 0.2);
    border: 1px solid #f2952e;

    .title {
      font-size: 20px;
      font-weight: bold;
    }

    .add-customer-btn {
      display: block;
      margin-right: 100px;
    }
  }
</style>
