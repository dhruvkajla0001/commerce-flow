const ctx = document.getElementById("revenueChart");

const revenueDataElement = document.getElementById("monthlyRevenueData");

if (ctx && revenueDataElement) {

    const revenueData = JSON.parse(revenueDataElement.textContent);

    const labels = revenueData.map(item => item.month_name);

    const values = revenueData.map(item => item.monthly_revenue);

    new Chart(ctx, {

        type: "line",

        data: {

            labels: labels,

            datasets: [

                {
                    label: "Monthly Revenue",

                    data: values,

                    borderWidth: 2,

                    tension: 0.3

                }

            ]

        }

    });

}

// ======================================================
// Order Status Pie Chart
// ======================================================

const orderStatusCanvas = document.getElementById("orderStatusChart");
const orderStatusElement = document.getElementById("orderStatusData");

if (orderStatusCanvas && orderStatusElement) {

    const orderStatus = JSON.parse(orderStatusElement.textContent);

    const labels = orderStatus.map(item => item.order_status);

    const values = orderStatus.map(item => item.total_orders);

    new Chart(orderStatusCanvas, {

        type: "pie",

        data: {

            labels: labels,

            datasets: [{

                label: "Orders",

                data: values

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

}

// ======================================================
// Top Products Bar Chart
// ======================================================

const topProductsCanvas = document.getElementById("topProductsChart");
const topProductsElement = document.getElementById("topProductsData");

if (topProductsCanvas && topProductsElement) {

    const topProducts = JSON.parse(topProductsElement.textContent);

    const labels = topProducts.map(item => item.product_category);

    const values = topProducts.map(item => item.total_revenue);

    new Chart(topProductsCanvas, {

        type: "bar",

        data: {

            labels: labels,

            datasets: [{

                label: "Revenue",

                data: values,

                borderWidth: 1

            }]

        },

        options: {

            responsive: true,

            indexAxis: "y",

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                x: {

                    beginAtZero: true

                }

            }

        }

    });

}

// ======================================================
// Revenue by State Chart
// ======================================================

const revenueByStateCanvas = document.getElementById("revenueByStateChart");
const revenueByStateElement = document.getElementById("revenueByStateData");

if (revenueByStateCanvas && revenueByStateElement) {

    const revenueByState = JSON.parse(revenueByStateElement.textContent);

    const labels = revenueByState.map(item => item.customer_state);

    const values = revenueByState.map(item => item.total_revenue);

    new Chart(revenueByStateCanvas, {

        type: "bar",

        data: {

            labels: labels,

            datasets: [{

                label: "Revenue",

                data: values,

                borderWidth: 1

            }]

        },

        options: {

            responsive: true,

            indexAxis: "y",

            plugins: {

                legend: {

                    display: false

                },

                title: {

                    display: true,

                    text: "Revenue by Customer State"

                }

            },

            scales: {

                x: {

                    beginAtZero: true,

                    title: {

                        display: true,

                        text: "Revenue"

                    }

                },

                y: {

                    title: {

                        display: true,

                        text: "State"

                    }

                }

            }

        }

    });

}