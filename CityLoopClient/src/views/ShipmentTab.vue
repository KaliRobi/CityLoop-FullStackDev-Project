<template>
  <main>
    <div class="city-loop-header">
      <div class="city-loop-name">
        <h1>City Loop Delivery</h1>
          <div class="shipment-amount">
              <p>Currently {{ countShipments }} shipment(s) in queue</p>
          </div>
        </div>
          <div class="logout">
            <button @click="logOut">Log Out</button>
          </div>
    </div>
    <div class="shipments-area">
      <div class="shipment-register-area">
    <div class="shipment-register-area-header">
        <h2>SHIPMENT REGISTER</h2>
    </div>
    <form @submit.prevent="createNewShipment" method="post">
    <div class="new-shipment-form" id="newShipmentForm" >
        <input type="text" id="trackingNumber" v-model="newShipment.trackingNumber" placeholder="Tracking Number" required>
        <input type="date" id="deliveryTime" v-model="newShipment.expectedDeliveryDate" placeholder="Expected Delivery Date" required>
        <input type="text" id="destination" v-model="newShipment.destination" placeholder="Destination" required >
        <select v-model="newShipment.modeOfTransport" required>
            <option disabled value="">Select a Transportation mode</option>
            <option v-for="mode in transportModes"   >
              {{ mode}}
            </option>
        </select>
        <input type="text" id="origin" v-model="newShipment.origin"  placeholder="Origin" required>
    </div>
    <div class="create-new-button-container">
        <button  id="newShipmentButton">New Shipment</button>
    </div>
    </form>
    </div>
    <div class="shipment-container">
        <table>
          <thead>
              <tr>
                  <th class="tracking-number">Tracking number</th>
                  <th class="delivery-time">Delivery date</th>
                  <th class="destination">Destination</th>
                  <th class="mode-of-transport">Mode of Transport</th>
                  <th class="origin">Origin</th>
                  <th>Actions</th>
              </tr>
          </thead>
          <tbody>
            <tr v-for="shipment in shipments" :key="shipment.trackingNumber" class="shipment-container">
                <td><p>{{ shipment.trackingNumber }}</p></td>
                <td><input type="text" v-model="shipment.expectedDeliveryDate" required ></td>
                <td><input type="text" v-model="shipment.destination" required></td>
                <td>
                  <select v-model="shipment.modeOfTransport" :value="shipment.modeOfTransport" required>
                    <option v-for="mode in transportModes" :key="mode.trackingNumber"  >
                      {{ mode}}
                    </option>
                  </select>
                </td>
                <td><input type="text" v-model="shipment.origin" required></td>
                <td>
                  <button @click="updateShipment(shipment.trackingNumber)">Update</button>
                  <button @click="deleteShipment(shipment.trackingNumber)">Delete</button>
                </td>
              </tr>
          </tbody>
      </table>
        <div class="paging-buttons">
            <button @click="prevPage"><< previous 5</button>
            <button @click="nextPage">next 5 >></button>
        </div>
    </div>
  </div> 
  </main>
</template>

<script setup>
import {ref, onMounted} from "vue"
import { useRouter } from 'vue-router'

const router = useRouter()

const shipments = ref([])
const countShipments = ref(0)
const transportModes = ref([])
const currentPage = ref(1) 


const headers = {
  'Content-type': 'application/json',
  'Authorization': `Bearer ${localStorage.getItem('access')}`
}

const domain = 'http://127.0.0.1:8000/'

const newShipment = ref({
  trackingNumber: '',
  expectedDeliveryDate: '',
  destination: '',
  modeOfTransport: '',
  origin: '',
}) 

const nextPage = () => {
  if (currentPage.value < Math.ceil(countShipments.value / 5 )){
  currentPage.value++ 
  fetchShipments() 
  }
} 


const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value-- 
    fetchShipments() 
  }
} 

const fetchShipments = async () => {
  const response = await fetch(`${domain}shipment-list/?page=${currentPage.value}`) 
  const data = await response.json() 
  shipments.value = data.results 
  countShipments.value = data.count
} 

const deleteShipment = async (trackingNumber) => {
  await fetch(`${domain}shipment/${trackingNumber}/delete/`, {
    method: 'DELETE',
    headers: headers , 
  }).then(response => response.json())
.catch((error) => console.error(error))
fetchShipments()
}


const updateShipment = async (trackingNumber) => {

  const shipmentToUpdate = shipments.value.find(s => s.trackingNumber === trackingNumber)
  await fetch(`${domain}shipment/${shipmentToUpdate.trackingNumber}/update/`, {
    method: 'PUT',  
    headers: headers, 
    body: JSON.stringify(shipmentToUpdate)
},).then(response => response.json())
.catch((error) => console.error(error)) 
fetchShipments()
}


const createNewShipment = async () => {
  fetch(`${domain}shipment/`, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(newShipment.value)
  }).then(response => response.json())
.catch((error) => console.error(error)) 
  fetchShipments()
}


const logOut = () =>{
      localStorage.removeItem('access')
      router.push({name: 'LoginTab'})   
}


onMounted( async () => {
  const shipmentsResponse = await fetch(`${domain}shipment-list/?page=${currentPage.value}`)
  const shipmentsData = await shipmentsResponse.json()
  shipments.value = shipmentsData.results

  const motResponse = await fetch(`${domain}transport-modes/`)
  const motList = await motResponse.json()
  transportModes.value = motList

  const amountResponse = await fetch(`${domain}shipment-list/`)
  const amountData = await amountResponse.json()
  countShipments.value = shipmentsData.count
}) 


</script>


<style scoped>

body {
  font-family: Arial, sans-serif ;
}

main {
  width: 80vw;
  margin: auto ;
}

.city-loop-header {
  display: flex ;
  justify-content: space-between ;
  align-items: center ;
  padding: 2vh 0 ;
  border-bottom: 1px solid #ddd ;
}

.city-loop-name h1 {
  margin: 0 ;
}

.user-info-container {
  display: flex ;
  gap: 2vw ;
}

.shipments-area {
  padding: 2vh 0 ;
}

.shipment-register-area {
  margin-bottom: 2vh ;
}

.new-shipment-form {
  display: flex ;
  gap: 1vw ;
  margin-bottom: 1vh ;
}

.new-shipment-form input {
  padding: 0.5vh ;
}

.create-new-button-container {
  display: flex ;
  justify-content: flex-end ;
}

.create-new-button-container button {
  padding: 0.5vh 1vw ;
}

.shipment-container {
  margin-top: 2vh ;
}

.shipment-container table {
  width: 100% ;
  border-collapse: collapse ;
}

.shipment-container th, .shipment-container td {
  border: 1px solid #ddd ;
  padding: 1vh ;
  text-align: left; 
}

.paging-buttons {
  display: flex ;
  justify-content: space-between ;
  margin-top: 2vh ;
}

</style>
