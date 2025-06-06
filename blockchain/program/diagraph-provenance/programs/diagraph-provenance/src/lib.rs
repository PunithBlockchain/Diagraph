use anchor_lang::prelude::*;

declare_id!("xtK5pAt3VfkkcYVjJxyoS7QVxN5za5Xj93PNCqLumtX");

#[program]
pub mod diagraph_provenance {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        msg!("Greetings from: {:?}", ctx.program_id);
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize {}
