# How to Produce MC Run Dependent

All the files you need to produce MC run dependent are in the directory: [data](https://gitlab.desy.de/belle2/data-production/data). It seems strange, but it's true, the secret of being a good MC manager is **not** asking too many questions.

In this directory, the interesting subdirectories are:

- **[mcrd_processing](https://gitlab.desy.de/belle2/data-production/data/-/tree/master/mcrd_processing?ref_type=heads)**: Contains the scripts and configuration files for processing MC run dependent data
- **[mcrd_local](https://gitlab.desy.de/belle2/data-production/data/-/tree/master/mcrd_local?ref_type=heads)**: Contains the scripts and configuration files for local processing of MC run dependent data

## mcrd_processing

In this directory, you will find the fundamental script to create the configuration files for the MCrd generation: [b2dp-prepare-mcrd](https://gitlab.desy.de/belle2/data-production/data/-/blob/master/mcrd_processing/b2dp-prepare-MCrd?ref_type=heads).

### Usage Steps

To use this script, you need to:

1. Setup a `basf2` release
2. Source the script: 
  ```bash
  cd .. && source setup.sh && cd mcrd_processing
  ```
3. Run the script: 
  ```bash
  ./b2dp-prepare-MCrd -c_d config_dataset.yaml -c_g example_generic.yaml
  ```

> **Tip**: Study the `b2dp-prepare-MCrd` script and what it does. It is the key to really understand how to produce MCrd.

where `config_dataset.yaml` is the configuration file for the dataset and `example_generic.yaml` is the configuration file for the generic production.

### Configuration files

#### Config Dataset
The **config_dataset** file includes the dataset list. One example is provided in the directory ([config_dataset_proc16.yaml](https://gitlab.desy.de/belle2/data-production/data/-/blob/master/mcrd_processing/config_dataset_proc16.yaml?ref_type=heads)). 

```yaml
experiment:
  12:
    proc16:
      beamEnergy: 4S
      sqrts: 10.580
      runsRange: 798-3904, 4272-5512, 5737-6437
      bgDataset: /belle/BG/release-08-00-04/DB00003159/BGOrel8/prod00040523/e0012/4S/%r/beambg
      bgLocal: /group/belle2/dataprod/BGOverlay/BGOrd/rel8/BGOExp12rel8/release-08-00-04/e0012/4S/r*/beambg/sub*/*
      GT:
        - mcrd_proc16
        - data_proc16
        - online
```

You have to modify the following parameters:

- **Experiment number** (`12` in this case)
- **Processing name** (*proc16*)
- **Beam energy**
- **Square root of s**
- **Runs range**
- **BGO dataset** paths (both grid and KEKCC)
- **Global Tags** (GTs) for MCrd production

##### Parameter Details:

- **Processing name**: Can be *`proc16`* or *`prompt`* according to the experiment
- **Beam energy**: Can be *`4S`*, *`4S_offres`* or *`5S_scan`*
- **Square root of s**: 
  - *`10.580`* for *`4S`*
  - *`10.520`* for *`4S_offres`*
  - *Variable* for *`5S_scan`*
- **Runs range**: Taken from the physics runs on the [RunDB](https://rundb.belle2.org/accounts/login/?next=/webview/runs/) page
- **BGO datasets**:
  - `bgDataset`: Path to the BGO dataset on the **grid**
  - `bgLocal`: Path to the BGO dataset on the **KEKCC**
  
  > **Note**: The Background Overlay are DelayedBhabha data generated during the data processing by the Data Manager. Usually he puts the paths on the Grid and on the KEKCC on xwiki Page of BGO. **Do NOT** change the layout (`%r` or `sub*/*`) of the paths, as this is approved by the Computing Team.

- **Global Tags (GTs)**: The GT chain consists of:
  - **MC Global Tag**: The Global Tag for MCrd processing *(more info later)*
  - **Data Global Tag**: The Global Tag for the data processing *(created during the calibration process)*
  - `online`: The Global Tag for the online processing *(taken from the online database)*

#### Config Generic

The **config_generic** file contains the configuration for the MCrd production. An example is provided in the directory ([proc16_chunk4_generic.yaml](https://gitlab.desy.de/belle2/data-production/mc/-/blob/master/MC16/MC16rd_proc16/release-08-00-10/MC16rd_proc16_chunk4/proc16_chunk4_generic.yaml?ref_type=heads)).

```yaml
# **** edit these variables according to your MC request ****
campaign : MC16rd_proc16
phase : eph3
gitlab : Issue-99
priority : 7

# **** do not edit from now on ****
release : release-08-00-10

## dataset parameters
# Common parameters
nstream: 4
max_reuse_rate: 200

eventTime : 2.0
eventsize : 10.0

# list of datasets and specific parameters
datasets:   
   uubar: 
      xsec: 1.605
      eventTime : 1.9071615
      eventsize : [8.0, 1.5]
      SystematicsCombinedHadronic : True
      SystematicsCombinedLowMulti : False
   ddbar: 
      xsec: 0.401
      eventTime : 1.9533566
      eventsize : [8.0, 1.5]
      SystematicsCombinedHadronic : True
      SystematicsCombinedLowMulti : False
   ssbar:
      xsec: 0.383
      eventTime : 1.9274689
      eventsize : [8.0, 1.5]
      SystematicsCombinedHadronic : True
      SystematicsCombinedLowMulti : False
   ccbar:
      xsec: 1.329
      eventTime : 2.3607397
      eventsize : [10.0, 1.5]
      SystematicsCombinedHadronic : True
      SystematicsCombinedLowMulti : False
   taupair:
      xsec: 0.919
      eventTime : 0.9297152
      eventsize : [5.0, 1.5, 0.05]
      SystematicsCombinedHadronic : True
      SystematicsCombinedLowMulti : True
   charged:
      xsec: 0.54
      eventTime : 3.1019499
      eventsize : [12.0, 1.5]
      SystematicsCombinedHadronic : True
      SystematicsCombinedLowMulti : False
   mixed:
      xsec: 0.51
      eventTime : 3.1564126
      eventsize : [12.0, 1.5]
      SystematicsCombinedHadronic : True
      SystematicsCombinedLowMulti : False
   mumu:
      xsec: 1.148
      eventTime : 0.5352069
      eventsize : [4.0, 0.05]
      SystematicsCombinedHadronic : False
      SystematicsCombinedLowMulti : True
   gg: 
      xsec: 5.1
      eventTime : 1.4
      eventsize : [3.0, 0.05]
      nstream: 2
      SystematicsCombinedHadronic : False
      SystematicsCombinedLowMulti : True
   ee:
      xsec: 295.8
      eventTime : 1.3
      eventsize : [1.0, 0.05]
      nstream: 0.1
      max_reuse_rate: 400
      SystematicsCombinedHadronic : False
      SystematicsCombinedLowMulti : True
   eeee:
      xsec: 39.55
      eventTime : 1.1
      eventsize : [3.0, 0.05]
      nstream: 1
      SystematicsCombinedHadronic : False
      SystematicsCombinedLowMulti : True
   eemumu:
      xsec: 18.83
      eventTime : 1.2
      eventsize : [4.0, 0.05]
      nstream: 1
      SystematicsCombinedHadronic : False
      SystematicsCombinedLowMulti : True
   llXX:
      xsec: 2.0053553
      eventTime : 1.5
      eventsize : [4.0, 0.05]
      nstream: 4
      SystematicsCombinedHadronic : False
      SystematicsCombinedLowMulti : True
   hhISR:
      xsec: 0.215644
      eventTime : 1.9
      eventsize : [5.0, 0.05]
      nstream: 1
      SystematicsCombinedHadronic : False
      SystematicsCombinedLowMulti : True

# **** tuning the GRID related parameters ****
CPUcorrectionFactor : 20.0
GRID_tuneFactor : 25200.0
# hours
jobLength : 8
```


Let's go into the details of this file:
- **campaign**: The name of the MC campaign, e.g., *`MC16rd_proc16`* or *`MC16rd_prompt`*. Change this according to your MC request.
- **phase**: The phase of the MC campaign, e.g., *`eph3`*. Usually, this is constant. 
- **gitlab**: The GitLab issue number related to the MC request, e.g., *`Issue-99`*. Change this according to your MC request.
- **priority**: The priority of the MC request. For *MC generic*, it is usually set to *`7`*. For *Data Processing*, it is set to *`9`*. You can leave it as is. Change it only for special requests.
- **release**: The release version of the MCrd production, e.g., *`release-08-00-10`*, for `proc16` and *`release-08-03-00`* for `prompt`. Change this according to your MC request.
- **nstream**: The number of streams for the MCrd production. The standard is 4, but this number can vary, according to the channel (e.g., 2 for `gg`, 0.1 for `ee`, etc.). Unless you have a specific request (for example 1 stream of an `ee` channel with a big retention rate in the steering file), leave it as is.
- **max_reuse_rate**: The maximum reuse rate for the MCrd production. The standard is 200, but this varies, according to the channel (e.g., 400 for `ee`, etc.). The **max_reuse_rate** is the maximum number of times where a BGO event is inserted into the MCrd.
  > **Note**: This is a problematic source parameter, maybe we will remove it in the future. There are events not generated, expecially in exp18, due to this reuse_rate cut and there are no big evidences that this is useful. Probably, we will remove it in the future.
- **eventTime** and **eventsize**: The average of CPU time and size per event. This is different for each channel and is calculated testing the MCrd producation locally (this number should change for a new release).
- **datasets**: The list of datasets and their specific parameters. Each dataset has:
  - **xsec**: The cross-section of the dataset in nb (change it if you change the generator, usually test it locally and the output of the generator tells you the cross section). The numbers of these cross-sections the standard ones with the default generators.
  - **eventTime**: See above
  - **eventsize**: See above
  - **nstream**: See above
  - **SystematicsCombinedHadronic** and **SystematicsCombinedLowMulti**: A boolean indicating if the dataset is combined with a systematic skims. In parallel with the generic production, we also produce a systematic skim. Some channels need the hadronic and other channels need the LowMulti. This adds to the steering file a snippet that produces the requested skim. If you want to produce the systematic skim, set it to `True`, otherwise set it to `False`.

GRID parameters (**do not** change them unless you have a specific request):  
- **CPUcorrectionFactor**
- **GRID_tuneFactor**
- **jobLength**: The length of the job in hours. This is usually set to 8.


### Output

If you run: 

```bash
./b2dp-prepare-MCrd -c_d config_dataset.yaml -c_g example_generic.yaml
```

You will get a directory called `f"{campaign}_{gitlabissue}"`, for example `MC16rd_proc16_Issue-99`. 

Inside this directory, you will find the following files:
- **config_dataset.yaml**: The dataset configuration file you provided
- **config_generic.yaml**: The generic configuration file you provided
- The logging output files
- The Information file, with all the MC details (channels, cross-sections, number of events, runs, etc.) 
- A directory for each experiment and energy, e.g., `exp12_4S`, containing:
  - The json files for each channel 
  - The steering files for each channel
  - The information file for that experiment and energy

### Launch the MCrd production

To submit the MCrd production, you need to run the following command:

```bash
gb2_prod_register json_file.json # this will give you a PROD_ID
gb2_prod_approve -p ${PROD_ID}
```

This will register the production and approve it. The production will be started by Miyake-san. You have to ask him to start the production on gitlab on the the Issue of the campaign, e.g., [*MC16rd_proc16 Data Production Campaign-2*](https://gitlab.desy.de/belle2/computing/distributed-computing/operations/data-production-campaigns/-/work_items/33)

> Tip: See all the commands of gb2_prod_* and see what they do. They are very useful to manage the MCrd production. For example, `gb2_prod_status -p ${PROD_ID}` will give you the status of the production, or, more helpfully, you can use:
> ```bash
> gb2_prod_status -p `seq 48572 48574`
> ```
> will give you the status of the productions with IDs from 48572 to 48574.


## Particular MCrd production

During your MC management, you will receive the strangest request you can imagine. Sometimes, you have to change the generator, change the cross-section, etc. Nobody will be always ready for all the possible requests.
Most of the time you have to use the `b2dp-prepare-MCrd` script, changing the options. Here there is the list of the most useful options (see the arg_parser of the script for more details):
- `-c_d` and `-c_g`: The configuration files for the dataset and the generic production, respectively. These are the most important options, as they define the dataset and the generic production.
- `-resub`: You cannot submit a production with the same name as an existing one. If you want to resubmit a production or submit a production with some differences, put the suffix with this command. Some examples:
  - `-resub _resub1`: when you have submitted a wrong production and you want to resubmit it with the same name
  - `-resub _whizard`: when you have to submit a production with a different generator, e.g., `Whizard` instead of `aafh`
  - Anything you want, but be careful to not use the same suffix as an existing production.
- `--templateJson`: You can use this option to specify a template JSON file to use for the production. The standard one is `MCrd_template.json`. Change it if you have to change some grid parameters, e.g., `MultiCore` production
- `--local`: You can use this option to run the production locally, without submitting it to the grid (more info later, see mcrd_local section)
- `--rel`: Standard one is 8. I hope no production will be done with a different release, but if you have to, you can use this option to specify the release version of the MCrd production. Most probably, when the standard release will be 9, nothing will change. But a production with release 6 is very different from a production with release 8.
- `--force`: This option will delete the existing directory and will recreate it.
- `-tmplt_str`: Change the template of the steering file. The standard one is `steering_mcrd_template.py`. Change it if you have to change some `basf2` snippet or a new generator. Generators are taken from [b2dp_generator.py](https://gitlab.desy.de/belle2/data-production/data/-/blob/master/mcrd_processing/b2dp_generators.py?ref_type=heads). Here, there are the standard generators for the MCrd production. If you want to use a different generator, you have to add it to this file and then use the `-tmplt_str` option to specify the new steering file.



## mrcd_local

Some request are very light for the grid and is much faster to run it at KEKCC, or you want to test the MCrd production locally. In this case, you can use the `mcrd_local` directory.

The script is very easy, since it is very similar to the grid one. You have to run the following command:

```bash
./b2dp-prepare-MCrd -c_d config_dataset.yaml -c_g example_generic.yaml --local
```
The `--local` option will produce a `yaml` file with all the information for the local production, instead of the json and the steering file for the grid production.

After this, go to the `mcrd_local` directory. 

Here, you have to create the steering file for your specific production. After this, launch the local production with the following command:

```bash
./b2dp-submit-local --eventType <eventType> --dslist ../mcrd_processing/ MC16rd_proc16_Issue-251/exp0035_prompt/<yaml_file>.yaml --steering <steering_file.py>  --queue <queue> (--rel6 --dry) 
```

Where:
- `<eventType>`: The type of the event, e.g., `charged`, `mixed`, `uubar`, `220204621` etc. This is the name of the dataset you want to produce.
- `<yaml_file>`: The name of the yaml file you created with the `b2dp-prepare-MCrd` script.
- `<steering_file.py>`: The name of the steering file you created for your specific production.
- `<queue>`: The name of the queue you want to use for the production (standard is `b2prod`).
- `--rel6`: If you want to run the production with release 6, use this option.
- `--dry`: If you want to run the production in dry mode, use this option.

To check the status of the local production, you can use the following command:

```bash
./b2dp-submit-local --eventType <eventType> --dslist ../mcrd_processing/ MC16rd_proc16_Issue-251/exp0035_prompt/<yaml_file>.yaml --steering <steering_file.py>  --queue <queue> --check
```

When the production is finished, and some of the jobs are failed, you can use the following command to resubmit the failed jobs:

```bash
./b2dp-submit-local --eventType <eventType> --dslist ../mcrd_processing/ MC16rd_proc16_Issue-251/exp0035_prompt/<yaml_file>.yaml --steering <steering_file.py>  --queue <queue> --resubmit
```

When all the jobs are finished, you can use the following command to merge the output files:

```bash
./b2dp-submit-local --eventType <eventType> --dslist ../mcrd_processing/ MC16rd_proc16_Issue-251/exp0035_prompt/<yaml_file>.yaml --queue <queue> --merge
```

This will merge all the output files into a small number of files.

Finally, put the merged files in the directory: 
```bash
/group/belle2/dataprod/dp_managers/{your_account}
```