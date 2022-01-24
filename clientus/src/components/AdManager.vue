<template>
  <div class="customers-manager">
    <ElCard
      class="box-card customer-card"
      v-for="(customer, customerKey) in customers"
      :key="customerKey"
    >
      <div
        slot="header"
        class="card-header"
      >
        <div class="customer-name">{{ customer.customerName }}</div>
      </div>
      <div
        v-if="!customer.billboards.length"
        class="customer-billboards-empty"
      >
        Нет биллбордов
      </div>

      <ul
        v-else
        class="customer-billboards"
      >
        <li
          class="billboard"
          v-for="(billboard, billboardKey) in customer.billboards"
          :key="billboardKey"
        >
          <div class="billboard-info">
            <div class="billboard-info"><span>Текст:<br></span> {{ billboard.info }} <br></div>
            <div class="billboard-address"><span>Адрес:<br></span> {{ billboard.address }}</div>
          </div>

          <ElButton @click="changeCustomer(customer.customerID, billboard.billboardID)">
            Настройки биллборда <i class="el-icon-s-tools el-icon-right"></i>
          </ElButton>
        </li>
      </ul>
      <ElButton @click="showBillboardDialog(customer.customerID)">
        Добавить биллборд <i class="el-icon-plus el-icon-right"></i>
      </ElButton>
    </ElCard>

    <AddBillboardDialog
      :dialogVisible.sync="billboardDialogVisible"
      :customerID="currentCustomerID"
      @close="closeBillboardDialog"
    />

    <BillboardSettings
      :dialogVisible.sync="billboardSettingsVisible"
      :customerID="currentCustomerID"
      :billboardID="currentBillboardID"
      @close="closeBillboardSettings"
    />
  </div>
</template>

<script>
import AddBillboardDialog from './AddBillboardDialog.vue';
import BillboardSettings from './BillboardSettings.vue';

export default {
  components: {
    AddBillboardDialog,
    BillboardSettings,
  },

  async created() {
    await this.$store.dispatch('getCustomers');
    this.customers = this.getCustomers;
  },

  data() {
    return {
      customers: [],
      billboardDialogVisible: false,
      billboardSettingsVisible: false,
      currentCustomerID: '',
      currentBillboardID: '',
    };
  },

  computed: {
    getCustomers() {
      return this.$store.getters.getCustomers;
    },
  },

  methods: {
    showBillboardDialog(ID) {
      this.currentCustomerID = ID;
      this.billboardDialogVisible = true;
    },

    closeBillboardDialog() {
      this.billboardDialogVisible = false;
      this.currentCustomerID = '';
    },

    changeCustomer(customerID, billboardID) {
      this.currentCustomerID = customerID;
      this.currentBillboardID = billboardID;
      this.billboardSettingsVisible = true;
    },

    async closeBillboardSettings() {
      this.billboardSettingsVisible = false;
      this.currentCustomerID = '';
      this.currentBillboardID = '';
    },
  },
};
</script>

<style lang="scss" scoped>
  .customers-manager {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    padding: 10px 0 0 0;
  }

  .customer-card {
    margin: 30px 30px 30px 0;
    width: 600px;
    background: #8d6914;

    .card-header {
      font-size: 18px;

      .customer-name {
        font-weight: bold;
      }

      .customer-name,
      .customer-type {
        margin: 5px 0;
      }
    }
  }

  .customer-billboards {
    margin: 10px 0;
    padding: 0;
    list-style: none;
    font-size: 18px;

    &-empty {
      margin: 10px 0;
      font-size: 18px;
      font-style: italic;
    }

    .billboard {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin: 5px 0;
      padding: 10px;
      border: 1px solid #cab2a7;
      border-radius: 5px;
      background: #cab2a7;

      &-info {
        display: flex;
        flex-direction: column;
        max-width: 300px;

        .billboard-info,
        .billboard-address {
          overflow: hidden;
          text-overflow: ellipsis;
        }
      }

      span {
        font-weight: bold;
      }
    }
  }
</style>
