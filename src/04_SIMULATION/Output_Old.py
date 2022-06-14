from Inputs import STOPS_OUTBOUND, CONTROLLED_STOPS, IDX_ARR_T, IDX_LOAD, IDX_PICK, IDX_DROP, IDX_HOLD_TIME, IDX_DEP_T, \
    TRIP_IDS_OUT, SCHED_DEP_OUT, IDX_SKIPPED
from Output_Processor import *
from File_Paths import *


class PostProcessor:
    def __init__(self, cp_trip_paths, cp_pax_paths, cp_tags, nr_reps, path_dir):
        self.colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'black', 'brown', 'purple', 'turquoise',
                       'gray']
        self.cp_trips, self.cp_pax, self.cp_tags = [], [], []
        for trip_path, pax_path, tag in zip(cp_trip_paths, cp_pax_paths, cp_tags):
            self.cp_trips.append(load(trip_path))
            self.cp_pax.append(load(pax_path))
            self.cp_tags.append(tag)
            self.nr_reps = nr_reps
            self.path_dir = path_dir

    def pax_times_fast(self, include_rbt=False):
        db_mean = []
        dbwt_mean = []
        wt_all_set = []
        rbt_od_set = []
        rbt_od_mean = []
        pc_wt_0_2_set = []
        pc_wt_2_4_set = []
        pc_wt_4_inf_set = []
        for pax in self.cp_pax:
            wt_set, dbm, dbwt, rbt_od, pc_wt_0_2, pc_wt_2_4, pc_wt_4_inf = get_pax_times_fast(pax,
                                                                                              len(STOPS_OUTBOUND),
                                                                                              include_rbt=include_rbt)
            wt_all_set.append(wt_set)
            db_mean.append(dbm)
            dbwt_mean.append(dbwt)
            rbt_od_set.append(rbt_od)
            rbt_od_mean.append(np.mean(rbt_od))
            pc_wt_0_2_set.append(pc_wt_0_2)
            pc_wt_2_4_set.append(pc_wt_2_4)
            pc_wt_4_inf_set.append(pc_wt_4_inf)
        results_d = {'method': self.cp_tags,
                     'wt_mean': [np.around(np.mean(wt_s), decimals=2) for wt_s in wt_all_set],
                     'err_wt_mean': [np.around(np.power(1.96, 2) * np.var(wt_s) / np.sqrt(self.nr_reps), decimals=3)
                                     for wt_s in wt_all_set],
                     'wt_median': [np.around(np.median(wt_s), decimals=2) for wt_s in wt_all_set],
                     'denied_per_mil': [round(db * 1000, 2) for db in db_mean],
                     'wt_0_2': pc_wt_0_2_set,
                     'wt_2_4': pc_wt_2_4_set,
                     'wt_4_inf': pc_wt_4_inf_set}
        if include_rbt:
            save(self.path_dir + 'rbt_numer.pkl', rbt_od_set)
        save(self.path_dir + 'wt_numer.pkl', wt_all_set)

        return results_d

    def headway(self, plot_bars=False, plot_cv=False, save_nc=False):
        cv_hw_set = []
        cv_all_reps = []
        cv_hw_tp_set = []
        hw_peak_set = []
        cv_mean_per_stop_set = []
        # for trips in self.cp_trips:
            # temp_cv_hw, cv_hw_tp, cv_hw_mean, hw_peak, cv_mean_per_stop = get_headway_from_trajectory_set(trips, IDX_ARR_T, STOPS_OUTBOUND,
            #                                                                             STOPS_OUTBOUND[50],
            #                                                                             controlled_stops=CONTROLLED_STOPS)
            # cv_hw_tp_set.append(cv_hw_tp)
            # cv_hw_set.append(temp_cv_hw)
            # cv_all_reps.append(cv_hw_mean)
            # hw_peak_set.append(hw_peak)
            # cv_mean_per_stop_set.append(cv_mean_per_stop)
        # if len(self.cp_tags) <= len(self.colors) and plot_cv:
        #     plot_headway(cv_mean_per_stop_set, STOPS_OUTBOUND, self.cp_tags, self.colors, pathname=self.path_dir + 'hw.png',
        #                  controlled_stops=CONTROLLED_STOPS[:-1])
        # if save_nc:
        #     save(self.path_dir + 'cv_hw_sim.pkl', cv_mean_per_stop_set[0])
        # results_hw = {'cv_h_tp': [np.around(np.mean(cv), decimals=2) for cv in cv_hw_tp_set],
        #               'err_cv_h_tp': [np.around(np.power(1.96, 2) * np.var(cv) / np.sqrt(self.nr_reps), decimals=3)
        #                               for cv in cv_hw_tp_set],
        #               'h_pk': [np.around(np.mean(hw), decimals=2) for hw in hw_peak_set],
        #               'std_h_pk': [np.around(np.std(hw), decimals=2) for hw in hw_peak_set],
        #               '95_h_pk': [np.around(np.percentile(hw, 95), decimals=2) for hw in hw_peak_set]}
        # # cv_hw_tp_set is for whisker plot
        # if plot_bars:
        #     tags = self.cp_tags
        #     idx_control_stops = [STOPS_OUTBOUND.index(cs) + 1 for cs in CONTROLLED_STOPS[:-1]]
        #     cv_tp_set = []
        #     for cv in cv_hw_set:
        #         cv_tp_set.append([cv[k] for k in idx_control_stops])
        #     x = np.arange(len(idx_control_stops))
        #     width = 0.1
        #     fig, ax = plt.subplots()
        #     print(cv_tp_set)
        #     bar1 = ax.bar(x - 3 * width / 2, cv_tp_set[0], width, label=tags[0], color='white', edgecolor='black')
        #     bar2 = ax.bar(x - width / 2, cv_tp_set[1], width, label=tags[1], color='silver', edgecolor='black')
        #     bar3 = ax.bar(x + width / 2, cv_tp_set[2], width, label=tags[2], color='gray', edgecolor='black')
        #     bar4 = ax.bar(x + 3 * width / 2, cv_tp_set[3], width, label=tags[3], color='black', edgecolor='black')
        #
        #     ax.set_ylabel('coefficient of variation of headway')
        #     ax.set_xlabel('control stop')
        #     ax.set_xticks(x, idx_control_stops)
        #     ax.legend()
        #
        #     fig.tight_layout()
        #     plt.savefig(self.path_dir + 'cv_hw_bar.png')
        #     plt.close()

        return

    def load_profile(self, plot_grid=False, plot_single=False):
        load_profile_set = []
        lp_std_set = []
        peak_load_set = []
        max_load_set = []
        min_load_set = []
        for trips in self.cp_trips:
            temp_lp, temp_lp_std, temp_peak_loads, max_load, min_load = load_from_trajectory_set(trips,
                                                                                                 STOPS_OUTBOUND, IDX_LOAD,
                                                                                                 STOPS_OUTBOUND[56])
            load_profile_set.append(temp_lp)
            lp_std_set.append(temp_lp_std)
            peak_load_set.append(temp_peak_loads)
            max_load_set.append(max_load)
            min_load_set.append(min_load)
        if plot_grid:
            plot_load_profile_grid(load_profile_set, max_load_set, min_load_set, STOPS_OUTBOUND, self.cp_tags,
                                   pathname=self.path_dir + 'lp_grid.png')
        if plot_single:
            plot_load_profile_benchmark(load_profile_set, STOPS_OUTBOUND, self.cp_tags, self.colors,
                                        pathname=self.path_dir + 'lp.png', controlled_stops=CONTROLLED_STOPS,
                                        x_y_lbls=['stop id', 'avg load per trip'], load_sd_set=lp_std_set)
        results_load = {'load_mean': [np.around(np.mean(peak_load), decimals=2) for peak_load in peak_load_set],
                        'std_load': [np.around(np.std(peak_load), decimals=2) for peak_load in peak_load_set],
                        '95_load': [np.around(np.percentile(peak_load, 95), decimals=2) for peak_load in peak_load_set]}
        return results_load

    def write_trajectories(self, only_nc=False, all_trajectories_out=None, trajectories_in=None):
        i = 0
        compare_trips = self.cp_trips
        if only_nc:
            compare_trips = [self.cp_trips[0]]
        for trips in compare_trips:
            write_trajectory_set(trips, 'out/trajectories/' + self.cp_tags[i] + '.csv', IDX_ARR_T, IDX_DEP_T,
                                 IDX_HOLD_TIME,
                                 header=['trip_id', 'stop_id', 'arr_t', 'dep_t', 'pax_load', 'ons', 'offs', 'denied',
                                         'hold_time', 'skipped', 'replication', 'arr_sec', 'dep_sec', 'dwell_sec'])
            i += 1
        return

    def control_actions(self):
        ht_ordered_freq_set = []
        skip_freq_set = []
        bounds = [(0, 20), (20, 40), (40, 60), (60, 80), (80, 100), (100, 120), (120, np.inf)]
        for i in range(len(self.cp_tags)):
            ht_dist, skip_freq = control_from_trajectory_set('out/trajectories/' + self.cp_tags[i] + '.csv',
                                                             CONTROLLED_STOPS)
            skip_freq_set.append(round(skip_freq, 1))
            ht_dist_arr = np.array(ht_dist)
            ht_ordered_freq = []
            for b in bounds:
                ht_ordered_freq.append(ht_dist_arr[(ht_dist_arr >= b[0]) & (ht_dist_arr < b[1])].size)
            ht_ordered_freq_set.append(ht_ordered_freq)
        results = {'skip_freq': skip_freq_set}
        return results

    def trip_times(self, keep_nc=False, plot=False):
        all_trip_times = []
        trip_time_mean_set = []
        trip_time_sd_set = []
        trip_time_95_set = []
        trip_time_85_set = []
        i = 0
        for trips in self.cp_trips:
            temp_trip_t = trip_time_from_trajectory_set(trips, IDX_DEP_T, IDX_ARR_T)
            all_trip_times.append(temp_trip_t)
            if i == 0 and keep_nc:
                temp_trip_t = trip_time_from_trajectory_set(self.cp_trips[0], IDX_DEP_T, IDX_ARR_T)
                save(self.path_dir + 'trip_t_sim.pkl', temp_trip_t)
            trip_time_mean_set.append(np.around(np.mean(temp_trip_t) / 60, decimals=2))
            trip_time_sd_set.append(np.around(np.std(temp_trip_t) / 60, decimals=2))
            trip_time_95_set.append(np.around(np.percentile(temp_trip_t, 95) / 60, decimals=2))
            trip_time_85_set.append(np.around(np.percentile(temp_trip_t, 90) / 60, decimals=2))
            i += 1
        if plot and len(all_trip_times) == 4:
            plot_4_trip_t_dist(all_trip_times, self.cp_tags, self.path_dir)
        save(self.path_dir + 'all_trip_t.pkl', all_trip_times)
        results_tt = {'tt_mean': trip_time_mean_set,
                      'tt_sd': trip_time_sd_set,
                      'tt_95': trip_time_95_set,
                      'tt_85': trip_time_85_set}
        return results_tt

    def validation(self):
        # temp_cv_hw, cv_hw_tp, cv_hw_mean, hw_peak = get_headway_from_trajectory_set(self.cp_trips[0], IDX_ARR_T, STOPS_OUTBOUND,
        #                                                                             STOPS_OUTBOUND[50],
        #                                                                             controlled_stops=CONTROLLED_STOPS)
        cv_hw_set = []
        plot_headway(cv_hw_set, STOPS_OUTBOUND, self.cp_tags, self.colors, pathname=self.path_dir + 'hw.png',
                     controlled_stops=CONTROLLED_STOPS[:-1])
        return

    def load_profile_validation(self):
        load_profile_set = []
        lp_std_set = []
        for trips in self.cp_trips:
            temp_lp, temp_lp_std, _, _, _ = pax_per_trip_from_trajectory_set(trips, IDX_LOAD, IDX_PICK, IDX_DROP, STOPS_OUTBOUND)
            load_profile_set.append(temp_lp)
            lp_std_set.append(temp_lp_std)
        lp_input = load('in/xtr/load_profile.pkl')
        load_profile_set.append(lp_input)
        plot_load_profile_benchmark(load_profile_set, STOPS_OUTBOUND, ['simulated', 'observed'], self.colors,
                                    pathname='out/validation/lp.png', x_y_lbls=['stop id', 'avg load per trip'])
        return

    def pax_profile_base(self):
        lp, _, _, ons, offs = pax_per_trip_from_trajectory_set(self.cp_trips[0], IDX_LOAD, IDX_PICK, IDX_DROP, STOPS_OUTBOUND)
        through = np.subtract(lp, offs)
        through[through < 0] = 0
        through = through.tolist()
        plot_pax_profile(ons, offs, lp, STOPS_OUTBOUND, through, pathname=self.path_dir + 'pax_profile_base.png',
                         x_y_lbls=['stop', 'passengers (per trip)',
                                   'through passengers and passenger load (per trip)'],
                         controlled_stops=CONTROLLED_STOPS[:-1])
        return


def count_load(file_dir, hw_threshold, count_skip=False):
    cs_load = []
    peak_load = []
    cs_hw = []
    peak_hw = []
    trajectory_set = load(file_dir)
    activate = False
    skipped = 0
    not_skipped = 0
    for trajectory in trajectory_set:
        last_t = None
        last_t_pk = None
        for trip in trajectory:
            for stop_info in trajectory[trip]:
                if stop_info[0] == STOPS_OUTBOUND[47]:
                    arr_t = stop_info[IDX_ARR_T]
                    if last_t:
                        hw = arr_t - last_t
                        if hw > hw_threshold:
                            if count_skip:
                                if stop_info[IDX_SKIPPED]:
                                    skipped += 1
                                else:
                                    not_skipped += 1
                            cs_load.append(stop_info[IDX_LOAD])
                            cs_hw.append(hw)
                            activate = True
                        else:
                            activate = False
                    last_t = deepcopy(arr_t)
                if activate and stop_info[0] == STOPS_OUTBOUND[56]:
                    peak_load.append(stop_info[IDX_LOAD])
                    arr_t = stop_info[IDX_ARR_T]
                    peak_hw.append(arr_t-last_t_pk)
                    activate = False
                if stop_info[0] == STOPS_OUTBOUND[56]:
                    last_t_pk = stop_info[IDX_ARR_T]

    avg_pk_load = np.around(np.mean(peak_load), decimals=2)
    avg_pk_hw = np.around(np.mean(peak_hw)/60, decimals=2)
    h_pk_load = np.around(np.percentile(peak_load, 95), decimals=2)
    h_pk_hw = np.around(np.percentile(peak_hw, 95)/60, decimals=2)
    avg_prev_hw = np.around(np.mean(cs_hw)/60, decimals=2)
    avg_prev_load = np.around(np.mean(cs_load), decimals=2)
    h_prev_hw = np.around(np.percentile(cs_hw, 95)/60, decimals=2)
    h_prev_load = np.around(np.percentile(cs_load, 95), decimals=2)

    if count_skip:
        skipped_freq = round(skipped / (skipped + not_skipped)*100, 2)
        return (avg_prev_hw,h_prev_hw), (avg_prev_load,h_prev_load), (avg_pk_hw,h_pk_hw), (avg_pk_load,h_pk_load), skipped_freq
    else:
        return (avg_prev_hw,h_prev_hw), (avg_prev_load,h_prev_load), (avg_pk_hw,h_pk_hw), (avg_pk_load,h_pk_load)


N_REPLICATIONS = 40


def weight_comparison(compute_rbt=False):
    prc_w = PostProcessor([path_tr_ddqn_ha3, path_tr_ddqn_ha5, path_tr_ddqn_ha7, path_tr_ddqn_ha9, path_tr_ddqn_ha11],
                          [path_p_ddqn_ha3, path_p_ddqn_ha5, path_p_ddqn_ha7, path_p_ddqn_ha9, path_p_ddqn_ha11],
                          tags_w, N_REPLICATIONS, path_dir_w)
    results_w = {}
    results_w.update(prc_w.pax_times_fast(include_rbt=compute_rbt))

    prc_w.write_trajectories()
    results_w.update(prc_w.control_actions())
    results_w.update(prc_w.trip_times())
    prc_w.headway()
    rbt_od_set = load(path_dir_w + 'rbt_numer.pkl')
    results_w.update({'rbt_mean': [np.around(np.mean(rbt), decimals=2) for rbt in rbt_od_set],
                      'rbt_median': [np.around(np.median(rbt), decimals=2) for rbt in rbt_od_set]})
    results_df = pd.DataFrame(results_w, columns=list(results_w.keys()))
    results_df.to_csv(path_dir_w + 'numer_results.csv', index=False)
    wt_all_set = load(path_dir_w + 'wt_numer.pkl')
    trip_t_all_set = load(path_dir_w + 'all_trip_t.pkl')
    plot_3_var_whisker(rbt_od_set, wt_all_set, trip_t_all_set,tags_w, path_dir_w + 'pax_times.png', 'reliability buffer time (min)',
                       'avg pax wait time (min)', 'trip time (min)', x_label=r'$W_{wait}$')
    return


def benchmark_comparison(compute_rbt=False):
    prc = PostProcessor([path_tr_nc_b, path_tr_eh_b, path_tr_ddqn_la_b,
                         path_tr_ddqn_ha_b],
                        [path_p_nc_b, path_p_eh_b, path_p_ddqn_la_b,
                         path_p_ddqn_ha_b], tags_b, N_REPLICATIONS,
                        path_dir_b)

    prc.pax_profile_base()
    results = {}
    results.update(prc.pax_times_fast(include_rbt=compute_rbt))

    rbt_od_set = load(path_dir_b + 'rbt_numer.pkl')
    results.update({'rbt_mean': [np.around(np.mean(rbt), decimals=2) for rbt in rbt_od_set],
                    'rbt_median': [np.around(np.median(rbt), decimals=2) for rbt in rbt_od_set]})
    prc.headway(plot_bars=True)
    results.update(prc.load_profile(plot_grid=True))
    results.update(prc.trip_times(keep_nc=True, plot=True))
    prc.write_trajectories()
    results.update(prc.control_actions())
    results_df = pd.DataFrame(results, columns=list(results.keys()))
    results_df.to_csv(path_dir_b + 'numer_results.csv', index=False)

    wt_all_set = load(path_dir_b + 'wt_numer.pkl')
    plot_2_var_whisker(rbt_od_set, wt_all_set, tags_b, path_dir_b + 'pax_times.png', 'reliability buffer time (min)',
                       'avg pax wait time (min)')
    return


def sensitivity_run_t(compute_rbt=False):
    prc = PostProcessor(
        [path_tr_eh_low_s1, path_tr_ddqn_la_low_s1_nr, path_tr_ddqn_la_low_s1, path_tr_ddqn_ha_low_s1_nr,
         path_tr_ddqn_ha_low_s1,
         path_tr_eh_base_s1, path_tr_ddqn_la_base_s1, path_tr_ddqn_ha_base_s1,
         path_tr_eh_high_s1, path_tr_ddqn_la_high_s1_nr, path_tr_ddqn_la_high_s1, path_tr_ddqn_ha_high_s1_nr,
         path_tr_ddqn_ha_high_s1],
        [path_p_eh_low_s1, path_p_ddqn_ha_low_s1_nr, path_p_ddqn_la_low_s1, path_p_ddqn_ha_low_s1_nr,
         path_p_ddqn_ha_low_s1,
         path_p_eh_base_s1, path_p_ddqn_la_base_s1, path_p_ddqn_ha_base_s1,
         path_p_eh_high_s1, path_p_ddqn_la_high_s1_nr, path_p_ddqn_la_high_s1, path_p_ddqn_ha_high_s1_nr,
         path_p_ddqn_ha_high_s1], tags_s1, N_REPLICATIONS, path_dir_s1)
    results = {}
    results.update(prc.pax_times_fast(include_rbt=compute_rbt))

    rbt_od_set = load(path_dir_s1 + 'rbt_numer.pkl')
    wt_all_set = load(path_dir_s1 + 'wt_numer.pkl')
    plot_sensitivity_whisker_run_t(rbt_od_set, wt_all_set, ['EH', 'DDQN-LA (NR)','DDQN-LA (R)', 'DDQN-HA (NR)', 'DDQN-HA (R)'],
                             ['cv: -20%', 'cv: base', 'cv: +20%'], ['EH', 'DDQN-LA', 'DDQN-HA'],
                             'reliability buffer time (min)', 'avg pax wait time (min)', path_dir_s1 + 'pax_times.png')
    results.update({'rbt_od': [np.around(np.mean(rbt), decimals=2) for rbt in rbt_od_set]})
    prc.headway()
    results_df = pd.DataFrame(results, columns=list(results.keys()))
    results_df.to_csv(path_dir_s1 + 'numer_results.csv', index=False)
    return


def sensitivity_compliance(compute_rbt=False):
    prc = PostProcessor([path_tr_eh_base_s2, path_tr_ddqn_la_base_s2, path_tr_ddqn_ha_base_s2,
                         path_tr_eh_80_s2, path_tr_ddqn_la_80_s2_nr, path_tr_ddqn_la_80_s2, path_tr_ddqn_ha_80_s2_nr,
                         path_tr_ddqn_ha_80_s2, path_tr_eh_60_s2, path_tr_ddqn_la_60_s2_nr, path_tr_ddqn_la_60_s2,
                         path_tr_ddqn_ha_60_s2_nr, path_tr_ddqn_ha_60_s2],
                        [path_p_eh_base_s2, path_p_ddqn_la_base_s2, path_p_ddqn_ha_base_s2,
                         path_p_eh_80_s2, path_p_ddqn_la_80_s2_nr, path_p_ddqn_la_80_s2, path_p_ddqn_ha_80_s2_nr,
                         path_p_ddqn_ha_80_s2, path_p_eh_60_s2, path_p_ddqn_la_60_s2_nr, path_p_ddqn_la_60_s2,
                         path_p_ddqn_ha_60_s2_nr, path_p_ddqn_ha_60_s2], tags_s2, N_REPLICATIONS,
                        path_dir_s2)
    results = {}
    results.update(prc.pax_times_fast(include_rbt=compute_rbt))
    rbt_od_set = load(path_dir_s2 + 'rbt_numer.pkl')
    wt_all_set = load(path_dir_s2 + 'wt_numer.pkl')
    plot_sensitivity_whisker_compliance(rbt_od_set, wt_all_set,
                                        ['EH', 'DDQN-LA (NR)', 'DDQN-LA (R)', 'DDQN-HA (NR)', 'DDQN-HA (R)'],
                                        ['base', '0.8', '0.6'], ['EH', 'DDQN-LA', 'DDQN-HA'],
                                        'reliability buffer time (min)', 'avg pax wait time (min)',
                                        path_dir_s2 + 'pax_times.png')
    results.update({'rbt_mean': [np.around(np.mean(rbt), decimals=2) for rbt in rbt_od_set],
                    'rbt_median': [np.around(np.median(rbt), decimals=2) for rbt in rbt_od_set]})
    prc.headway()
    results_df = pd.DataFrame(results, columns=list(results.keys()))
    results_df.to_csv(path_dir_s2 + 'numer_results.csv', index=False)
    return


def fancy_plots():
    wt_all_set2 = load(path_dir_s1 + 'wt_numer.pkl')
    nr_replications = 40
    nr_methods = 3
    nr_scenarios = 3
    idx = [0, 2, 4, 5, 6, 7, 8, 10, 12]
    wt = list(np.array(wt_all_set2)[idx].flatten())

    method = (['EH'] * nr_replications + ['RL-LA'] * nr_replications + ['RL-HA'] * nr_replications) * nr_scenarios
    tt_var = ['low'] * nr_replications * nr_methods + ['base'] * nr_replications * nr_methods + ['high'] * nr_replications * nr_methods

    df_dict = {'tt_var': tt_var, 'method': method, 'wt': wt}
    df = pd.DataFrame(df_dict)
    sns.set(style='darkgrid')
    sns.boxplot(x='tt_var', y='wt', hue='method', data=df, showfliers= False)
    plt.ylabel('mean wait time (min)')
    plt.xlabel('run time variability')
    plt.savefig('out/compare/sensitivity run times/wt_fancy.png')
    plt.close()

    wt_set = load(path_dir_s2 + 'wt_numer.pkl')

    nr_replications = 40
    nr_methods = 3
    nr_scenarios = 3
    idx = [0, 1, 2, 3, 5, 6, 8, 9, 11]
    wt = list(np.array(wt_set)[idx].flatten())

    method = (['EH'] * nr_replications + ['RL-LA'] * nr_replications + ['RL-HA'] * nr_replications) * nr_scenarios
    compliance = [100] * nr_replications * nr_methods + [80] * nr_replications * nr_methods + [60] * nr_replications * nr_methods

    df_dict = {'compliance': compliance, 'method': method, 'wt': wt}
    df = pd.DataFrame(df_dict)
    sns.set(style='darkgrid')
    sns.boxplot(x='compliance', y='wt', hue='method', data=df, showfliers= False)
    plt.legend('')
    plt.xlabel('degree of compliance (%)')
    plt.ylabel('mean wait time (min)')
    plt.savefig('out/compare/sensitivity compliance/wt_fancy.png')
    plt.close()

    return