import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def one_time_draw_traj(save_path):
    # Raw data in string format (copy-pasted from your example)
    data = """
    bfs	node	32	5.50	5.208200E-05	3.858590E-04	1.705139E-01	4.085449E-01	2.209000E-06	174.675871
    bfs	node	64	5.97	5.221900E-05	3.860150E-04	1.752428E-01	4.151959E-01	2.213000E-06	174.430637
    bfs	node	128	8.81	5.263500E-05	3.864710E-04	2.459027E-01	6.031555E-01	3.267000E-06	118.295378
    bfs	node	256	14.75	5.355700E-05	3.874730E-04	3.654295E-01	9.584173E-01	5.107000E-06	75.870961
    bfs	node	512	26.22	5.551100E-05	3.895910E-04	6.013237E-01	1.665355E+00	8.770000E-06	44.423147
    bfs	node	1024	49.85	7.086400E-05	4.052630E-04	1.084709E+00	3.064763E+00	1.632400E-05	24.826207
    bfs	node	2048	99.70	7.128800E-05	4.061410E-04	2.055414E+00	3.757521E+00	1.630000E-05	24.916626
    bfs	node	4096	199.44	7.097200E-05	4.067330E-04	4.079310E+00	5.261405E+00	1.730600E-05	23.502427
    bfs	node	8192	401.16	7.170100E-05	4.092770E-04	7.896844E+00	7.979804E+00	1.725100E-05	23.724828
    bfs	node	16384	807.14	7.221500E-05	4.134130E-04	1.580543E+01	1.387267E+01	1.878100E-05	22.012300
    fir	length	128	1.15	8.242000E-06	8.406700E-05	8.024466E-02	1.351868E-01	8.140000E-07	103.276413
    fir	length	256	2.17	8.266000E-06	8.411700E-05	9.878703E-02	2.389559E-01	1.416000E-06	59.404661
    fir	length	512	4.21	7.697000E-06	8.360200E-05	1.423738E-01	2.605959E-01	1.432000E-06	58.381285
    fir	length	1024	8.34	7.705000E-06	8.371800E-05	2.227682E-01	3.131135E-01	1.470000E-06	56.951020
    fir	length	2048	16.75	7.707000E-06	8.387000E-05	3.906387E-01	4.097133E-01	1.496000E-06	56.062834
    fir	length	4096	33.61	7.707000E-06	8.417200E-05	7.469848E-01	6.466794E-01	1.437000E-06	58.574809
    fir	length	8192	67.25	7.739000E-06	8.481000E-05	1.419443E+00	1.107887E+00	1.462000E-06	58.009576
    fir	length	16384	136.70	7.859000E-06	8.613800E-05	2.801522E+00	2.214942E+00	2.605000E-06	33.066411
    fir	length	32768	274.44	8.529000E-06	8.922400E-05	5.599120E+00	4.715824E+00	6.581000E-06	13.557818
    fir	length	65536	549.09	1.782500E-05	1.033520E-04	1.069411E+01	9.624698E+00	1.396000E-05	7.403438
    kmeans	points	8	7.89	8.168200E-05	2.914070E-04	2.213053E-01	4.942735E-01	2.618000E-06	111.309015
    kmeans	points	16	8.95	8.102700E-05	2.908610E-04	2.455359E-01	4.980374E-01	2.580000E-06	112.736822
    kmeans	points	32	16.11	1.217470E-04	4.018350E-04	3.851676E-01	6.704806E-01	3.237000E-06	124.138091
    kmeans	points	64	29.06	1.632710E-04	5.136310E-04	6.129872E-01	8.344207E-01	3.406000E-06	150.801820
    kmeans	points	128	67.80	2.003500E-04	6.213270E-04	1.387139E+00	1.637862E+00	5.686000E-06	109.273127
    kmeans	points	256	141.55	1.737780E-04	5.961010E-04	2.829623E+00	2.596687E+00	6.853000E-06	86.983949
    kmeans	points	512	284.21	1.793970E-04	6.044050E-04	5.556240E+00	4.670055E+00	9.400000E-06	64.298404
    kmeans	points	1024	567.82	1.906900E-04	6.210670E-04	1.111059E+01	9.441663E+00	1.915900E-05	32.416462
    matrixmultiplication	x	8	2.88	3.567000E-06	8.955100E-05	1.042970E-01	1.678721E-01	9.250000E-07	96.811892
    matrixmultiplication	x	16	3.14	3.567000E-06	8.976500E-05	1.121429E-01	1.960577E-01	1.075000E-06	83.502326
    matrixmultiplication	x	32	7.57	1.296400E-05	9.946500E-05	1.931653E-01	3.101048E-01	1.385000E-06	71.815884
    matrixmultiplication	x	64	12.44	2.145800E-05	1.085630E-04	3.128153E-01	5.192013E-01	2.328000E-06	46.633591
    matrixmultiplication	x	128	22.29	3.931000E-05	1.276270E-04	5.095562E-01	9.443686E-01	4.272000E-06	29.875234
    matrixmultiplication	x	256	41.95	7.813600E-05	1.688690E-04	9.052486E-01	2.300075E+00	1.131600E-05	14.923029
    matrixmultiplication	x	512	81.76	1.528180E-04	2.483830E-04	1.703007E+00	4.602803E+00	2.307800E-05	10.762761
    matrixmultiplication	x	1024	162.36	3.016020E-04	4.068310E-04	3.240185E+00	9.504984E+00	4.838600E-05	8.408031
    matrixmultiplication	x	2048	322.50	6.281280E-04	7.526850E-04	6.340489E+00	1.924414E+01	9.889500E-05	7.610951
    matrixmultiplication	x	4096	646.11	1.443968E-03	1.607181E-03	1.257572E+01	3.882282E+01	1.961920E-04	8.191878
    matrixtranspose	width	4	0.30	5.327000E-06	7.510700E-05	5.245952E-02	4.703680E-02	3.600000E-07	208.630556
    matrixtranspose	width	8	0.36	5.373000E-06	7.526900E-05	6.194506E-02	5.079113E-02	3.770000E-07	199.652520
    matrixtranspose	width	16	0.52	5.294000E-06	7.527100E-05	6.246364E-02	5.443646E-02	3.540000E-07	212.629944
    matrixtranspose	width	32	1.38	5.566000E-06	7.586500E-05	8.448914E-02	9.262820E-02	4.830000E-07	157.070393
    matrixtranspose	width	64	4.76	6.478000E-06	7.768300E-05	1.496370E-01	2.574516E-01	1.353000E-06	57.415373
    matrixtranspose	width	128	18.98	7.591000E-06	8.242500E-05	4.283386E-01	9.528478E-01	5.049000E-06	16.325015
    matrixtranspose	width	256	77.41	1.093400E-05	1.002610E-04	1.569575E+00	3.980736E+00	2.050300E-05	4.890065
    matrixtranspose	width	512	316.39	1.659200E-05	1.639810E-04	5.960592E+00	1.577345E+01	8.197100E-05	2.000476
    pagerank	iterations	1	2.39	5.572000E-06	1.208110E-04	1.041056E-01	9.179600E-02	3.900000E-07	309.771795
    pagerank	iterations	2	4.95	9.287000E-06	1.700330E-04	1.487134E-01	1.201097E-01	4.060000E-07	418.800493
    pagerank	iterations	4	9.31	1.650100E-05	2.682570E-04	2.523038E-01	2.171668E-01	5.550000E-07	483.345946
    pagerank	iterations	8	18.96	3.087300E-05	4.646490E-04	4.515092E-01	3.997232E-01	7.820000E-07	594.180307
    pagerank	iterations	16	37.03	5.984700E-05	8.576630E-04	8.369397E-01	7.538915E-01	1.186000E-06	723.155987
    pagerank	iterations	32	76.48	1.163650E-04	1.642287E-03	1.587435E+00	1.526125E+00	2.506000E-06	655.341979
    pagerank	iterations	64	153.16	2.320370E-04	3.214147E-03	3.195992E+00	3.274371E+00	5.925000E-06	542.472068
    pagerank	iterations	128	307.27	4.605930E-04	6.354969E-03	6.309457E+00	6.318626E+00	1.208500E-05	525.855937
    pagerank	iterations	256	636.89	9.199720E-04	1.263906E-02	1.206011E+01	1.284136E+01	2.363700E-05	534.714938
    pagerank	node	2	6.24	5.670100E-05	8.544550E-04	1.901566E-01	2.501368E-01	9.860000E-07	866.587221
    pagerank	node	4	10.96	5.744500E-05	8.551990E-04	2.885302E-01	3.186584E-01	1.093000E-06	782.432754
    pagerank	node	8	20.32	5.891700E-05	8.566770E-04	4.581170E-01	4.501415E-01	1.062000E-06	806.663842
    pagerank	node	16	38.11	5.956500E-05	8.573850E-04	8.215527E-01	7.449093E-01	1.199000E-06	715.083403
    pagerank	node	32	76.71	6.193200E-05	8.599630E-04	1.530536E+00	1.373546E+00	2.078000E-06	413.841675
    pagerank	node	64	151.23	6.137800E-05	8.594570E-04	3.105327E+00	2.718748E+00	3.475000E-06	247.325755
    pagerank	node	128	291.83	6.202100E-05	8.601510E-04	6.113089E+00	5.301365E+00	6.593000E-06	130.464280
    pagerank	node	256	561.55	6.606200E-05	8.643410E-04	1.155055E+01	1.050989E+01	1.322200E-05	65.371426
    relu	length	1024	1.70	3.917000E-06	7.418300E-05	8.779822E-02	7.537307E-02	4.050000E-07	183.167901
    relu	length	2048	3.26	3.933000E-06	7.449900E-05	1.157831E-01	1.478585E-01	7.130000E-07	104.486676
    relu	length	4096	6.50	3.965000E-06	7.513500E-05	1.793048E-01	2.755037E-01	1.329000E-06	56.534989
    relu	length	8192	12.82	4.035000E-06	7.641900E-05	3.037598E-01	5.496509E-01	2.561000E-06	29.839516
    relu	length	16384	25.68	4.219000E-06	7.901900E-05	5.491499E-01	1.077983E+00	5.025000E-06	15.725174
    relu	length	32768	51.45	5.361000E-06	8.499300E-05	1.093396E+00	2.279193E+00	1.043000E-05	8.148897
    relu	length	65536	104.13	8.187000E-06	9.748300E-05	2.000763E+00	4.548335E+00	2.121300E-05	4.595437
    relu	length	131072	209.54	1.368700E-05	1.223110E-04	4.030045E+00	8.986218E+00	4.302800E-05	2.842591
    relu	length	262144	420.33	2.460700E-05	1.719710E-04	8.114926E+00	1.784399E+01	8.622700E-05	1.994399
    relu	length	524288	845.22	4.616300E-05	2.708450E-04	1.587886E+01	3.566629E+01	1.723660E-04	1.571337
    spmv	dim	16	0.31	5.820000E-06	1.362230E-04	5.969088E-02	4.261113E-02	3.220000E-07	423.052795
    spmv	dim	32	0.39	6.870000E-06	1.374350E-04	5.604681E-02	4.621918E-02	3.240000E-07	424.182099
    spmv	dim	64	0.49	6.266000E-06	1.369750E-04	5.853035E-02	5.736340E-02	3.340000E-07	410.104790
    spmv	dim	128	1.17	7.298000E-06	1.381070E-04	7.438163E-02	8.093907E-02	4.290000E-07	321.927739
    spmv	dim	256	3.66	8.446000E-06	1.395730E-04	1.326016E-01	1.279486E-01	6.590000E-07	211.795144
    spmv	dim	512	16.08	1.043600E-05	1.423510E-04	3.405794E-01	3.235927E-01	1.213000E-06	117.354493
    spmv	dim	1024	83.61	1.667300E-05	1.513510E-04	1.603890E+00	1.270210E+00	3.885000E-06	38.957786
    spmv	dim	2048	442.76	2.587300E-05	1.704710E-04	7.997761E+00	6.414412E+00	1.936600E-05	8.802592
    """

    # Convert raw data to a DataFrame
    lines = [line.strip() for line in data.strip().split("\n") if line.strip()]
    columns = ["job_name", "param_arg", "params", "ratio"]
    parsed_data = []

    for line in lines:
        parts = line.split()
        job_name = parts[0]
        param_arg = parts[1]
        params = int(parts[2])
        ratio = float(parts[-1])  # Assuming Ratio is the last column
        parsed_data.append([job_name, param_arg, params, ratio])

    df = pd.DataFrame(parsed_data, columns=columns)

    # Plotting
    plt.figure(figsize=(24, 16))
    unique_trajectories = df.groupby(["job_name", "param_arg"])
    colors = plt.cm.tab10(np.linspace(0, 1, len(unique_trajectories)))

    for (index, ((job_name, param_arg), group)) in enumerate(unique_trajectories):
        # group = group.sort_values(by="params")  # Ensure data is ordered by params
        x_values = np.log2(group["params"])  # Log2 for consistent spacing
        # print(f"x_values: {x_values}")
        y_values = group["ratio"]
        plt.plot(x_values, y_values, label=f"{job_name}-{param_arg}", marker="x", color=colors[index], linewidth=3, markersize=10, alpha=0.7)

    # Customizing the x-axis for $2^n$ ticks
    print(sorted(np.log2(df["params"].unique())))
    print([f"$2^{{{int(np.log2(param))}}}$" for param in sorted(df["params"].unique())])
    plt.xticks(
        ticks=sorted(np.log2(df["params"].unique())),
        labels=[f"$2^{{{int(np.log2(param))}}}$" for param in sorted(df["params"].unique())],
        fontsize=20,
    )
    plt.yscale("log")
    y_ticks = [2 ** i for i in range(int(np.log2(df["ratio"].min())), int(np.log2(df["ratio"].max())) + 1)]
    plt.yticks(
        ticks=y_ticks,
        labels=[f"{tick}" for tick in y_ticks],
        fontsize=20,
    )

    plt.xlabel("Parameters (log scale)", fontsize=20)
    plt.ylabel("Ratio", fontsize=20)

    plt.title("Trajectories for Different {Task Name}-{Arg Name}", fontsize=30)
    plt.legend(fontsize=20)
    plt.grid(True, linestyle="--", alpha=0.6)
    # plt.show()
    plt.tight_layout()
    plt.savefig(save_path, dpi=400)


if __name__ == "__main__":
    one_time_draw_traj("benchmarks.png")
