use anchor_lang::prelude::*;

declare_id!("xtK5pAt3VfkkcYVjJxyoS7QVxN5za5Xj93PNCqLumtX"); // Replaced after deployment

#[program]
pub mod diagraph_provenance {
    use super::*;

    pub fn log_data(ctx: Context<LogData>, source: String, id: String, data_hash: String) -> Result<()> {
        let record = &mut ctx.accounts.record;
        record.source = source;
        record.id = id;
        record.data_hash = data_hash;
        record.timestamp = Clock::get()?.unix_timestamp;
        Ok(())
    }
}

#[derive(Accounts)]
pub struct LogData<'info> {
    #[account(init, payer = signer, space = 8 + 32 + 64 + 64 + 8)]
    pub record: Account<'info, ProvenanceRecord>,
    #[account(mut)]
    pub signer: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[account]
pub struct ProvenanceRecord {
    pub source: String,      // e.g., "PubMed"
    pub id: String,         // e.g., "34614373"
    pub data_hash: String,  // SHA256 hash
    pub timestamp: i64,     // UNIX timestamp
}