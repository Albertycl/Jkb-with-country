
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/ParentLandingPage.vue') },
      { path: '/alert_for_each_folder/:id', name: "alert_for_each_folder", component: () => import('pages/alert_for_each_folder.vue') },
      { path: '/alert_for_incoming_isp_monitoring/:infra_and_isp', name: "alert_for_incoming_isp_monitoring", component: () => import('pages/alert_for_incoming_isp_monitoring.vue') },
      { path: '/child30_threshold/', name: "child30_threshold", component: () => import('pages/child30_threshold.vue') },
      { path: '/child15_top_right_possilbe_incoming_or_outgoing/', name: "child15_top_right_possilbe_incoming_or_outgoing", component: () => import('pages/child15_top_right_possilbe_incoming_or_outgoing.vue') },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
