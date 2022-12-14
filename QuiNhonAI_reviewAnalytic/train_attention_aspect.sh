CUDA_VISIBLE_DEVICES="2" python3 custom_train.py \
  --model_name_or_path /media/Z/namlh31/review-roberta-large-40 \
  --train_file /media/Z/namlh31/QuiNhon_hackathon/hackathon_data/train_processed.json \
  --validation_file /media/Z/namlh31/QuiNhon_hackathon/hackathon_data/dev_processed.json \
  --do_eval \
  --do_train \
  --model_type attention \
  --do_lower_case \
  --evaluation_strategy steps \
  --eval_steps 200 \
  --save_steps 500 \
  --save_total_limit 5 \
  --max_seq_length 128 \
  --per_device_train_batch_size 16 \
  --per_device_eval_batch_size 64 \
  --learning_rate 2e-5 \
  --num_train_epochs 10 \
  --overwrite_cache \
  --overwrite_output_dir \
  --output_dir /media/Z/namlh31/QuiNhon_hackathon/results/viroberta-large-attention-part2-128/ \
  --cache_dir /home/namlh31/cache/